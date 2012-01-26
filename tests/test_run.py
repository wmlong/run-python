import unittest
from run import Command
from run_python import PythonDriver

class RunTest_base(unittest.TestCase):
    
    def setUp(self):
        #TODO: set cwd
        self.command = Command(self.ARGV)
        self.driver = PythonDriver(self.command)


class RunTest_run(RunTest_base):
    
    ARGV = ['run', 'name', '1']

    def test(self):
        self.driver.process()
        
        
class RunTest_help(RunTest_base):
    
    ARGV = ['run', '-h']

    def test(self):
        self.driver.process()