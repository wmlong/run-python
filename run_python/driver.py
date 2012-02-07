import os
import subprocess
from run.drivers.base import BaseDriver
from run.library.reader import Reader
from run.library.property import cachedproperty

class PythonDriver(BaseDriver):
    
    CONNECTOR_FILE = ['files', 'connector.py']    

    def process(self):
        return subprocess.call(['python', '-c', self._connector], 
                               env=self._environ)

    @cachedproperty
    def _environ(self):
        environ = {
            'RUN_COMMAND': self._command.json,           
        }
        environ.update(os.environ)
        return environ
    
    @cachedproperty
    def _connector(self):
        return self._reader.read(*self.CONNECTOR_FILE)
    
    @cachedproperty
    def _reader(self):
        return Reader(os.path.dirname(__file__))