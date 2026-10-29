#!/usr/bin/env python3
"""Execute approved experiment command, capture logs, inputs, outputs and commit."""
import argparse,datetime,hashlib,json,platform,subprocess,sys,uuid
from pathlib import Path
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for c in iter(lambda:f.read(1048576),b''):h.update(c)
 return h.hexdigest()
def run(project,command,inputs,outputs):
 project=project.resolve(strict=True)
 if not command:raise ValueError('Explicit command required')
 for p in inputs+outputs:
  if p.is_absolute() or '..' in p.parts:raise ValueError('Project-relative paths only')
 inp={str(p):digest(project/p) for p in inputs if (project/p).is_file()}
 if len(inp)!=len(inputs):raise FileNotFoundError('Missing input data')
 stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
 d=project/'experiment'/'runs'/(stamp+'-'+uuid.uuid4().hex[:8]);d.mkdir(parents=True)
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (d/'stdout.log').open('wb') as out,(d/'stderr.log').open('wb') as err:cp=subprocess.run(command,cwd=project,stdout=out,stderr=err,check=False)
 artifacts={str(p):digest(project/p) for p in outputs if (project/p).is_file()}
 try:commit=subprocess.run(['git','rev-parse','HEAD'],cwd=project,capture_output=True,text=True,timeout=5).stdout.strip()
 except (OSError,subprocess.TimeoutExpired):commit=None
 record={'id':d.name,'status':'completed' if cp.returncode==0 else 'failed','exit_code':cp.returncode,'start_utc':start,'end_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':command,'python':sys.version,'platform':platform.platform(),'git_commit':commit,'data_sha256':inp,'output_sha256':artifacts,'stdout_log':str((d/'stdout.log').relative_to(project)),'stderr_log':str((d/'stderr.log').relative_to(project))}
 (d/'run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 return d,cp.returncode
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('--input',type=Path,action='append',default=[]);p.add_argument('--result',type=Path,action='append',default=[]);p.add_argument('command',nargs=argparse.REMAINDER)
 a=p.parse_args();cmd=a.command[1:] if a.command[:1]==['--'] else a.command
 d,status=run(a.project,cmd,a.input,a.result);print('RUN',d);sys.exit(status)
