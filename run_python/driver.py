import os
import subprocess
from run.drivers.base import BaseDriver
from run.library.property import cachedproperty

class PythonDriver(BaseDriver):
    
    CONNECTOR = ['files', 'connector.py']    

    def process(self):
        return subprocess.call(['python', self._connector], 
                               env=self._environ)

    @cachedproperty
    def _environ(self):
        environ = os.environ.copy()
        environ['RUN_COMMAND'] = self._command.json
        return environ
    
    @cachedproperty
    def _connector(self):
        return os.path.join(os.path.dirname(__file__),
                            *self.CONNECTOR)