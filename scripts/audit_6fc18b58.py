#!/usr/bin/env python3
"""Structural row inventory, not legal/source-content verification. Standard library only."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse
ROOT = Path(__file__).resolve().parents[1]
class Rows(HTMLParser):
    def __init__(self):
        super().__init__(); self.rows=[]; self.row=None
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='tr': self.row={'text':'','urls':[],'data':False}
        if self.row is not None:
            if tag=='td': self.row['data']=True
            if tag=='a' and a.get('href','').startswith(('https://','http://')): self.row['urls'].append(a['href'])
    def handle_data(self, text):
        if self.row is not None: self.row['text']+=text+' '
    def handle_endtag(self, tag):
        if tag=='tr' and self.row is not None:
            if self.row['data']: self.rows.append(self.row)
            self.row=None

def official(url):
    h=(urlparse(url).hostname or '').lower()
    return h.endswith('.gov') or h in {'coveredca.com','www.coveredca.com','hbex.coveredca.com','board.coveredca.com'}

def main():
    pages=[]; missing=[]; total=0
    for p in sorted(ROOT.rglob('*.html')):
        rel=p.relative_to(ROOT)
        if any(x in rel.parts for x in ('.git','_site','node_modules')): continue
        parser=Rows(); parser.feed(p.read_text())
        count=0
        for i,row in enumerate(parser.rows,1):
            total+=1
            if not any(official(u) for u in row['urls']):
                count+=1; missing.append({'page':str(rel),'data_row':i,'claim_excerpt':' '.join(row['text'].split())[:220],'external_links':row['urls'],'status':'needs review: no direct official-domain link in this row'})
        pages.append({'page':str(rel),'data_rows':len(parser.rows),'rows_without_direct_official_link':count})
    report={'date':'2026-10-18','scope':'All published HTML data rows; direct external official-domain link presence ONLY. Links via source registers are not resolved. A link is not proof of content, availability, or legal accuracy. Missing links include editorial/status rows, not necessarily substantive errors.','pages':pages,'total_data_rows':total,'rows_without_direct_official_link':len(missing),'needs_review':missing}
    out=ROOT/'audit-6fc18b58.json'; out.write_text(json.dumps(report,indent=2)+'\n')
    # Publish every exception as a readable list, not an unsupported claim table.
    from html import escape
    page = ROOT/'audit-6fc18b58.html'
    if page.exists():
        text = page.read_text()
        start = '<!-- row-inventory:start -->'; end = '<!-- row-inventory:end -->'
        if start in text and end in text:
            items = ''.join('<li><a href="'+escape(r['page'], quote=True)+'">'+escape(r['page'])+'</a>, data row '+str(r['data_row'])+': '+escape(r['claim_excerpt'])+'</li>' for r in missing)
            block = '<p><strong>'+str(len(pages))+' pages / '+str(total)+' data rows / '+str(len(missing))+' rows without a direct official-domain row link.</strong> These are structural review flags, not established factual errors. Each excerpt below identifies a row for review. No missing authority is invented.</p><details><summary>Show every row-link exception ('+str(len(missing))+')</summary><ol>'+items+'</ol></details>'
            a=text.index(start)+len(start); b=text.index(end,a)
            page.write_text(text[:a]+'\n'+block+'\n'+text[b:])
    print(f"{len(pages)} pages; {total} data rows; {len(missing)} lack direct official-domain row links. Full inventory: {out.name}")
if __name__=='__main__': main()
