import os

class Connector(object):
    
    def __init__(self, environ):
        self.help = environ['RUN_HELP']
        self.filename = environ['RUN_FILENAME']
        self.function = environ['RUN_FUNCTION']
        self.arguments = environ['RUN_ARGUMENTS']
        
    def process(self):
        pass
    
    def _run(self):
        execfile(self.filename)
        exec '{function}({arguments})'.format(function=self.function,
                                              arguments=self.arguments)
    
    def _help(self):
        execfile(self.filename)
        functions = []
        for obj in locals().values():
            if getattr(obj, '__module__', None) == '__main__':
                functions.append(obj)
        if self.function:                                   
            pass

def main():    
    connector = Connector(os.environ)
    connector.run()
    
if __name__ == '__main__':
    main()