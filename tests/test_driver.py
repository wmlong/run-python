import unittest
from run import Command
from run_python import PythonDriver

class PythonDriverTest(unittest.TestCase):
    
    def setUp(self):
        self.argv = ['run', 'name', '1']
        self.command = Command(self.argv)
        self.driver = PythonDriver(self.command)
    
    def test(self):
        self.driver.process()