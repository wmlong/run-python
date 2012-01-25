import os
import sys

class Connector(object):
    
    def __init__(self, environ):
        self.help = environ['RUN_HELP']
        self.filename = environ['RUN_FILENAME']
        self.function = environ['RUN_FUNCTION']
        self.arguments = environ['RUN_ARGUMENTS']
        
    def process(self):
        if not self.help:
            self._run()
        else:
            self._help()
    
    def _run(self):
        execfile(self.filename)
        exec '{function}({arguments})'.format(function=self.function,
                                              arguments=self.arguments)
    
    def _help(self):
        execfile(self.filename)
        runfile = ConnectorRunfile(locals())
        if not self.function:
            sys.stdout.write(runfile.reference)
        else:
            sys.stdout.write(runfile.functions[self.function].reference)
        
        
class ConnectorRunfile(object):
    
    def __init__(self, namespace):
        self.functions = []
        for obj in locals().values():
            if getattr(obj, '__module__', None) == '__main__':
                self.functions.append(ConnectorFunction(obj))
        
    @property
    def reference(self):
        lines = []
        for function in self.functions:
            lines.append(function.reference)
        return '\n\n'.join(lines)


class ConnectorFunction(object):
    
    def __init__(self, function):
        self.function = function

    @property
    def reference(self):
        lines = []
        if self.signature:
            lines.append(self.signature)
        else:
            lines.append(self.name)
        if self.description:
            lines.append(self.description)
        return '\n'.join(lines)
    
    
def main():    
    connector = Connector(os.environ)
    connector.run()
    
if __name__ == '__main__':
    main()