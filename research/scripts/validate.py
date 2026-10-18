"""Validate source coverage, unresolved blanks, unique IDs, local links and page output."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
D=json.loads(Path('data/findings.json').read_text())
assert len({r['id'] for r in D['rows']})==len(D['rows'])
for r in D['rows']:
 assert r['sources'],r['id']
 for s in r['sources']:assert s in D['sources']
 if r['status']=='Unverified':assert r['value']=='',r['id']
for s in D['sources'].values():
 host=urlparse(s['url']).hostname
 assert host.endswith('.gov') or host.endswith('.coveredca.com'),host
class Check(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[];self.rows=[];self.inrow=False;self.external=False
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  if tag=='tr':self.inrow=True;self.external=False
  if tag=='a' and a.get('href','').startswith('https://'):self.external=True
  for key in ['href','src']:
   if key in a:self.links.append(a[key])
 def handle_endtag(self,tag):
  if tag=='tr':self.rows.append(self.external);self.inrow=False
for p in Path('.').glob('*.html'):
 c=Check();c.feed(p.read_text());assert len(c.ids)==len(set(c.ids)),p
 assert all(c.rows[1:]),f'Row without official source: {p}'
 for link in c.links:
  u=urlparse(link)
  if u.scheme:continue
  target=Path(unquote(u.path)) if u.path else p
  assert target.exists(),f'{p}: {link}'
  if u.fragment:
   z=Check();z.feed(target.read_text());assert u.fragment in z.ids,(p,link)
print(f'PASS: {len(D["rows"])} source-linked findings; {len(list(Path(".").glob("*.html")))} pages; local links and fragments intact.')
print('External sources checked by research retrieval; this test does not certify remote uptime or personal eligibility.')
