import os
import sys
import json
import inspect
 
def main():    
    connector = Connector(os.environ)
    connector.process()
         
class Connector(object):
    
    def __init__(self, environ):
        self.command = json.loads(environ['RUN_COMMAND'])
        
    def process(self):
        if not self.command['help']:
            self._run()
        else:
            self._help()
    
    def _run(self):
        execfile(self.command['filename'])
        exec ('{function}({arguments})'.
              format(function=self.command['function'],
                     arguments=self.command['arguments']))
    
    def _help(self):
        execfile(self.command['filename'])
        confile = ConnectorFile(locals())
        if not self.command['function']:
            sys.stdout.write(confile.help)
        else:
            sys.stdout.write(confile.
                             functions[self.command['function']].
                             help)
        
        
class ConnectorFile(object):
    
    def __init__(self, namespace):
        self.functions = {}
        for name, obj in locals().items():
            if getattr(obj, '__module__', None) == '__main__':
                self.functions[name] = ConnectorFunction(obj)
        
    @property
    def help(self):
        return '\n'.join(function.name 
                         for function in self.functions)


class ConnectorFunction(object):
    
    def __init__(self, function):
        self.function = function
    
    @property
    def name(self):
        return self.function.func_name
    
    @property
    def help(self):
        return '\n'.join(self._signature+self._docstring)

    @property
    def _signature(self):
        return [('{name}({argstring})'.
                 format(name=self.name,
                        argstring=self._argstring))]
    
    @property
    def _docstring(self):
        docstring = []
        getdoc = inspect.getdoc(self.function)
        if getdoc:
            docstring.append(getdoc)
        return docstring
  
    @property
    def _argstring(self):
        return ', '.join(self._argstring_general+
                         self._argstring_varargs+
                         self._argstring_keywords)

    @property
    def _argstring_general(self):
        general = []
        if self._argspec.defaults:
            defaults = list(self._argspec.defaults)
        else:
            defaults = []
        for arg in reversed(self._argspec.args):
            if not defaults:
                general.insert(0, arg)
            else:
                default = repr(defaults.pop())
                general.insert(0, '{arg}={default}'.
                                  format(arg=arg, 
                                         default=default))
        return general
    
    @property
    def _argstring_varargs(self):
        varargs = []
        if self._argspec.varargs:
            varargs.append('*{varargs}'.
                           format(varargs=self._argspec.varargs))
        return varargs
    
    @property
    def _argstring_keywords(self):
        keywords = []
        if self._argspec.keywords:
            keywords.append('**{keywords}'.
                            format(keywords=self._argspec.keywords))
        return keywords

    @property
    def _argspec(self):
        return inspect.getargspec(self.function)

    
if __name__ == '__main__':
    main()           

import unittest

class ConnectorFunctionTest(unittest.TestCase):
    
    def setUp(self):
        def function(a, b='default', *args, **kwargs): 
            """docstring"""
            pass
        self.confunc = ConnectorFunction(function)
        
    def test_name(self):
        self.assertEqual(self.confunc.name, 'function')
        
    def test_help(self):
        self.assertEqual(
            self.confunc.help, 
            "function(a, b='default', *args, **kwargs)\ndocstring")

        
class ConnectorFunctionTest_empty_function(unittest.TestCase):
    
    def setUp(self):
        def empty():
            pass
        self.confunc = ConnectorFunction(empty)
    
    def test_name(self):
        self.assertEqual(self.confunc.name, 'empty') 
        
    def test_help(self):
        self.assertEqual(self.confunc.help, 'empty()')               