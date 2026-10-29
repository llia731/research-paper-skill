#!/usr/bin/env python3
"""Check essential research project artifacts."""
import argparse,json
from pathlib import Path
REQUIRED=['.research/project.yaml','.research/workflow-state.yaml','.research/evidence-index.json','.research/literature-index.json']
def check(project):
 missing=[x for x in REQUIRED if not (project/x).is_file()]
 for f in ['.research/evidence-index.json','.research/literature-index.json']:
  p=project/f
  if p.exists():
   try:json.loads(p.read_text(encoding='utf-8'))
   except (ValueError,UnicodeError):missing.append(f+':invalid JSON')
 return missing
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('project',type=Path);a=p.parse_args()
 issues=check(a.project);print('OK' if not issues else '\n'.join(issues));raise SystemExit(0 if not issues else 2)
