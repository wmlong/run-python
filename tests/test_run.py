import os
import sys
import unittest
from run.library.patcher import Patcher
from run.scripts.run import run
from .fixtures import process

class RunTest(unittest.TestCase):
    
    PATCH = {
        'process.cwd': os.path.dirname(__file__)          
    }
    
    def setUp(self):
        #TODO: set cwd
        self.patcher = Patcher(globals())
        self.patcher.patch(self.PATCH)
        
    def tearDown(self):
        self.patcher.restore()


class RunTest_run(RunTest):
    
    PATCH = RunTest.PATCH.copy()
    PATCH.update({
        'sys.argv': ['run', 'name', '1'],        
    })
    
    def test(self):
        run()
        
      
class RunTest_help(RunTest):
    
    PATCH = RunTest.PATCH.copy()
    PATCH.update({
        'sys.argv': ['run', '-h'],        
    })
            
    def test(self):
        self.assertRaises(SystemExit, run)
                
        
class RunTest_help_function(RunTest):
    
    PATCH = RunTest.PATCH.copy()
    PATCH.update({
        'sys.argv': ['run', 'name', '-h'],        
    })
            
    def test(self):
        run() 