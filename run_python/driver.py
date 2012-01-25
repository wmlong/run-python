import os
import re
import subprocess
from run import Settings
from run.drivers.helper import HelperDriver
from run.library.reader import Reader
from run.library.property import cachedproperty

class PythonDriver(HelperDriver):
    
    CONNECTOR = ['files', 'connector.py']    

    def _run(self):
        return subprocess.call(['python', '-c', self._connector], 
                               env=self._environ)
    
    @property
    def _runfile(self):
        pass

    @cachedproperty
    def _environ(self):
        environ = {
            'filename': self.command.filename,
            'function': self.command.function,
            'arguments': self.command.arguments,           
        }
        environ.update(os.environ)
        return environ
    
    @cachedproperty
    def _connector(self):
        return self._reader.read(*self.CONNECTOR)
    
    @cachedproperty
    def _reader(self):
        return Reader(os.path.dirname(__file__))