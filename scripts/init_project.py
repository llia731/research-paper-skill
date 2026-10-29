#!/usr/bin/env python3
"""Initialize research state without overwriting user files."""
import argparse,shutil
from pathlib import Path
def init(project):
 root=Path(__file__).resolve().parents[1]; project=project.resolve()
 for file,dest in [('project.yaml','.research/project.yaml'),('workflow-state.yaml','.research/workflow-state.yaml'),('evidence-index.json','.research/evidence-index.json'),('claim-evidence.json','.research/claim-evidence.json'),('literature-index.json','.research/literature-index.json'),('issues.md','.research/issues.md'),('experiment-manifest.yaml','experiment/experiment-manifest.yaml'),('figure-manifest.json','figures/figure-manifest.json')]:
  p=project/dest;p.parent.mkdir(parents=True,exist_ok=True)
  if not p.exists():shutil.copyfile(root/'templates'/file,p)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('project',type=Path);init(p.parse_args().project)
