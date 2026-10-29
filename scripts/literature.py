#!/usr/bin/env python3
"""Import Zotero CSV/JSON; optional Crossref DOI-title verification."""
import argparse,csv,hashlib,json,re,urllib.request,urllib.parse
from pathlib import Path
DOI=re.compile(r'10\.\d{4,9}/[^\s<>"\']+',re.I)
def norm(x):
 x=re.sub(r'^https?://(?:dx\.)?doi\.org/|^doi\s*:\s*','',str(x or '').strip(),flags=re.I)
 m=DOI.search(x)
 return m.group(0).rstrip('.,;)]}').lower() if m else None
def items(p):
 if p.suffix.lower()=='.csv':
  with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
 x=json.loads(p.read_text(encoding='utf-8'))
 if isinstance(x,dict):x=x.get('items')
 if not isinstance(x,list):raise ValueError('Expected Zotero JSON list')
 return x
def make(src,out,verify=False):
 old=json.loads(out.read_text(encoding='utf-8')) if out.exists() else {}
 records={i['id']:i for i in old.get('records',[])}
 for raw in items(src):
  i=raw.get('data',raw)
  doi=norm(i.get('DOI') or i.get('doi') or i.get('url'))
  title=str(i.get('title') or i.get('Title') or '').strip()
  if not (doi or title):continue
  key=doi or 'title:'+hashlib.sha256(title.casefold().encode()).hexdigest()[:16]
  authors=i.get('authors') or i.get('Author') or i.get('creators') or []
  rec={'id':key,'doi':doi,'title':title,'authors':authors,'date':i.get('date') or i.get('Date') or '', 'verification':'unverified'}
  if verify and doi:
   try:
    url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='')
    req=urllib.request.Request(url,headers={'User-Agent':'ResearchPaperSkill/0.3'})
    with urllib.request.urlopen(req,timeout=12) as resp:meta=json.load(resp)['message']
    remote=(meta.get('title') or [''])[0]
    rec['verified_title']=remote
    norm_title=lambda s:re.sub(r'\W+','',s.casefold())
    rec['verification']='matched' if norm_title(title) and norm_title(title)==norm_title(remote) else 'needs_review'
   except Exception as exc:rec['verification']='lookup_failed';rec['error']=type(exc).__name__
  records[key]=rec
 out.parent.mkdir(parents=True,exist_ok=True)
 out.write_text(json.dumps({'schema_version':1,'records':sorted(records.values(),key=lambda x:x['id'])},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return len(records)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--verify-crossref',action='store_true')
 a=p.parse_args();print('RECORDS',make(a.source,a.output,a.verify_crossref))
