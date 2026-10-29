import sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from init_project import init
from check_project import check
class FrameworkTest(unittest.TestCase):
 def test_init_and_check(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);init(p);self.assertEqual(check(p),[])
 def test_nonoverwrite(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);init(p);f=p/'.research'/'project.yaml';f.write_text('custom');init(p);self.assertEqual(f.read_text(),'custom')
