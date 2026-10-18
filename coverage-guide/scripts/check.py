#!/usr/bin/env python3
"""Fail on missing local targets, incomplete evidence, bad IDs or generated drift."""
import json, subprocess
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
root=Path(__file__).resolve().parents[1]
d=json.loads((root/'research/findings.json').read_text())
allowed={'www.cms.gov','www.govinfo.gov','www.medicaid.gov','www.dhcs.ca.gov','www.coveredca.com','www.healthcare.gov','www.irs.gov','bphc.hrsa.gov','www.congress.gov'}
ids=set(); total=0
for s in d['sources'].values():
    u=urlsplit(s['url'])
    assert u.scheme=='https' and u.hostname in allowed,s
    assert s['excerpt'] and s['locator']
for r in d['summary']+[r for s in d['sections'] for r in s['rows']]:
    total+=1
    assert r['id'] not in ids,r['id']
    ids.add(r['id'])
    assert r['sources'] and all(x in d['sources'] for x in r['sources']),r
    assert r['evidence'] and r['note'] and r['status'],r
    assert r['value'] or r['status']=='Needs review',r
for r in next(s for s in d['sections'] if s['slug']=='flagged')['rows']:
    assert r['value']=='',r
class Parser(HTMLParser):
    def __init__(self): super().__init__();self.links=[];self.ids=set();self.inrow=False;self.body=False;self.rowlinks=[];self.rows=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'id' in a:
            assert a['id'] not in self.ids,a['id']
            self.ids.add(a['id'])
        if tag=='tbody':self.body=True
        if tag=='tr' and self.body:self.inrow=True;self.rowlinks=[]
        if tag in ('a','link','script'):
            url=a.get('href',a.get('src',''));self.links.append(url)
            if self.inrow and url.startswith('https://'):self.rowlinks.append(url)
    def handle_endtag(self,tag):
        if tag=='tr' and self.inrow:self.rows.append(self.rowlinks);self.inrow=False
        if tag=='tbody':self.body=False
pages={}
for p in [root/'index.html',*sorted((root/'pages').glob('*.html'))]:
    parser=Parser();parser.feed(p.read_text());pages[p]=parser
    assert all(parser.rows),f'Unsourced row: {p}'
links=0
for p,parser in pages.items():
    for link in parser.links:
        u=urlsplit(link)
        if u.scheme or u.netloc:continue
        target=(p.parent/unquote(u.path)).resolve() if u.path else p
        assert target.is_relative_to(root) and target.exists(),(p,link)
        if u.fragment and target in pages:assert u.fragment in pages[target].ids,(p,link)
        links+=1
before={p:p.read_bytes() for p in pages}
subprocess.run(['python','scripts/build.py'],cwd=root,check=True)
assert all(p.read_bytes()==content for p,content in before.items()),'Generated files drifted; commit rebuilt output'
print(f'PASS: {total} finding rows, {len(d["sources"])} official source records, {len(pages)} pages, {links} local references, blank unresolved values, deterministic build. External HTTP checks NOT performed.')
