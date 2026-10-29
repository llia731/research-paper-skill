#!/usr/bin/env python3
"""Reproducible plots with input/output SHA256 sidecar."""
import argparse,csv,hashlib,json,math
from pathlib import Path
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plot(source,xkey,ykeys,output,kind='line',units=None):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 with source.open(encoding='utf-8-sig',newline='') as fh:
  reader=csv.DictReader(fh)
  if xkey not in (reader.fieldnames or []) or any(y not in reader.fieldnames for y in ykeys):raise ValueError('Missing columns')
  rows=list(reader)
 if not rows:raise ValueError('Empty input')
 xs=[row[xkey] for row in rows];series={}
 for y in ykeys:
  vals=[float(row[y]) for row in rows]
  if not all(math.isfinite(v) for v in vals):raise ValueError('Non-finite data')
  series[y]=vals
 fig,ax=plt.subplots(figsize=(6.4,4),layout='constrained')
 for i,(name,vals) in enumerate(series.items()):
  if kind=='bar':
   import numpy as np
   pos=np.arange(len(xs));n=len(series);ax.bar(pos+(i-(n-1)/2)*0.8/n,vals,width=0.8/n,label=name);ax.set_xticks(pos,xs)
  else:ax.plot(xs,vals,marker='o',label=name)
 ax.set_xlabel(xkey);ax.set_ylabel(units or 'Value')
 if len(series)>1:ax.legend()
 ax.grid(axis='y',alpha=.2);output.parent.mkdir(parents=True,exist_ok=True)
 fig.savefig(output);plt.close(fig)
 meta={'source':str(source.resolve()),'source_sha256':sha(source),'output':str(output.resolve()),'output_sha256':sha(output),'columns':{'x':xkey,'y':ykeys},'kind':kind,'point_count':len(rows)}
 sidecar=Path(str(output)+'.json');sidecar.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return sidecar
def verify(sidecar):
 m=json.loads(sidecar.read_text(encoding='utf-8'));s=Path(m['source']);o=Path(m['output'])
 return s.is_file() and o.is_file() and sha(s)==m['source_sha256'] and sha(o)==m['output_sha256']
if __name__=='__main__':
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest='action',required=True)
 g=sp.add_parser('generate');g.add_argument('csv',type=Path);g.add_argument('--x',required=True);g.add_argument('--y',action='append',required=True);g.add_argument('--output',type=Path,required=True);g.add_argument('--kind',choices=['line','bar'],default='line');g.add_argument('--units')
 v=sp.add_parser('verify');v.add_argument('manifest',type=Path)
 a=p.parse_args()
 if a.action=='generate':print('MANIFEST',plot(a.csv,a.x,a.y,a.output,a.kind,a.units))
 else:
  ok=verify(a.manifest);print('VALID' if ok else 'CHANGED_OR_MISSING');raise SystemExit(0 if ok else 2)
