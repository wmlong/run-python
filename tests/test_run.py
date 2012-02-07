import sys
import unittest
from run.library.patcher import Patcher
from run.scripts.run import run

class RunTest(unittest.TestCase):
    
    def setUp(self):
        #TODO: set cwd
        self.patcher = Patcher(globals())
        self.patcher.patch(self.PATCH)
        
    def tearDown(self):
        self.patcher.restore()


class RunTest_run(RunTest):
    
    PATCH = {
        'sys.argv': ['run', 'name', '1'],        
    }
    
    def test(self):
        run()

      
class RunTest_help(RunTest):
    
    PATCH = {
        'sys.argv': ['run', '-h'],        
    }
            
    def test(self):
        self.assertRaises(SystemExit, run)