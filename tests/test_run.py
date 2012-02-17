import os
import sys
import unittest
from run.library.patcher import Patcher
from run.scripts.run import run
from .fixtures import process

#Environ
sys, process


#Tests
class RunTest(unittest.TestCase):
    
    PATCH = {
        'process.cwd': os.path.dirname(__file__)          
    }
    
    def setUp(self):
        self.patcher = Patcher(globals())
        self.patcher.patch(self.PATCH)
        
    def tearDown(self):
        self.patcher.restore()
        
      
class RunTest_run(RunTest):
    
    PATCH = RunTest.PATCH.copy()
    PATCH.update({
        'sys.argv': ['run', 'function_normal', '1', 'b=test words'],        
    })
    
    def test(self):
        run()   

  
class RunTest_list(RunTest):
    
    PATCH = RunTest.PATCH.copy()
    PATCH.update({
        'sys.argv': ['run'],        
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
        'sys.argv': ['run', 'function_normal', '-h'],        
    })
            
    def test(self):
        run() 