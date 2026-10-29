#!/usr/bin/env python3
"""Page-anchored PDF text extraction without external upload."""
import argparse,hashlib,json
from pathlib import Path
def extract(pdf,out,query=None):
 try:import fitz
 except ImportError as exc:raise RuntimeError('pip install pymupdf') from exc
 d=fitz.open(pdf);pages=[]
 for number,page in enumerate(d,1):
  txt=page.get_text('text')
  if query and query.casefold() not in txt.casefold():continue
  pages.append({'page':number,'text':txt[:12000],'characters':len(txt)})
 result={'pdf_file':pdf.name,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'page_count':len(d),'pages':pages,'note':'Check scans, tables, figures and equations manually.'}
 out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('pdf',type=Path);p.add_argument('--output',type=Path,required=True);p.add_argument('--query')
 a=p.parse_args();print('PAGES',len(extract(a.pdf,a.output,a.query)['pages']))
