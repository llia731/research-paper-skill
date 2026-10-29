import sys,tempfile,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from literature import norm,make
from plot_results import plot,verify
class VersionTests(unittest.TestCase):
 def test_doi(self):self.assertEqual(norm('https://doi.org/10.1000/ABC'), '10.1000/abc')
 def test_import(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'z.csv').write_text('Title,DOI\nExample,10.1000/abc\n',encoding='utf-8')
   out=p/'refs.json';self.assertEqual(make(p/'z.csv',out),1);self.assertEqual(len(json.loads(out.read_text())['records']),1)
 def test_plot_hash(self):
  try:import matplotlib
  except ImportError:self.skipTest('matplotlib unavailable')
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);source=p/'scores.csv';source.write_text('epoch,score\n1,0.1\n2,0.2\n')
   s=plot(source,'epoch',['score'],p/'figure.pdf');self.assertTrue(verify(s))
   source.write_text('epoch,score\n1,0.2\n');self.assertFalse(verify(s))
