import sys, pathlib, unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'scripts'))
from smoke import evaluate, dependency_inventory

class SmokeParserTests(unittest.TestCase):
    def test_ready_and_enabled(self):
        lines=['[INFO]: [Nullgate] Enabling Nullgate v0.1.0-alpha.4.21','[INFO]: Done (12.34s)! For help, type "help"','[INFO]: Stopping server']
        r=evaluate(lines,0,{'PacketEvents':False,'Floodgate':False,'Geyser-Spigot':False})
        self.assertEqual('PASS',r['verdict']);self.assertFalse(r['production_certified'])
    def test_abi_error_fails(self):
        r=evaluate(['[INFO]: [Nullgate] Enabling Nullgate','[INFO]: Done (13.3s)!','java.lang.NoSuchMethodError: bad'],0,{})
        self.assertEqual('FAIL',r['verdict'])
    def test_strict_dependencies(self):
        r=evaluate(['[INFO]: [Nullgate] enabled','[INFO]: Done (14.1s)!'],0,{'PacketEvents':True,'Floodgate':False,'Geyser-Spigot':True},True)
        self.assertEqual('FAIL',r['verdict'])
    def test_crash_or_missing_enable_fails(self):
        self.assertEqual('FAIL',evaluate(['[INFO]: Done (14.1s)!'],1,{})['verdict'])
if __name__=='__main__':unittest.main()
