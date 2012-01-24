import os
import re
import subprocess
from run import Settings
from run.drivers.helper import HelperDriver
from run.library.reader import Reader
from run.library.property import cachedproperty

class PythonDriver(HelperDriver):

    def process(self):
        return subprocess.call(self._rendered, shell=True)

    @cachedproperty
    def _rendered(self):
        return (self._reader.read('command').
                format(module=self._module,
                       function=self.command.function,
                       arguments=self.command.arguments))
        
    @cachedproperty
    def _module(self):
        return re.sub(Settings.LANGUAGS['python'], '', 
                      self.command.filename)
    
    @cachedproperty
    def _reader(self):
        return Reader(os.path.dirname(__file__), 'templates')