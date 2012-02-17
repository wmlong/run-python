import os
import sys
import json
import types
import inspect
 
def main():    
    connector = Connector(os.environ)
    connector.process()
         
class Connector(object):
    
    def __init__(self, environ):
        self._command = json.loads(environ['RUN_COMMAND'])
        
    def process(self):
        if not self._command['ishelp']:
            if self._command['function']:
                self._run()
            else:
                self._list()
        else:
            self._help()
    
    def _run(self):
        eval('self._module.{function}({arguments})'.
             format(function=self._command['function'],
                    arguments=self._arguments), globals(), locals())
        
    def _list(self):
        confile = ConnectorFile(self._module)
        sys.stdout.write(confile.list)

    def _help(self):
        confile = ConnectorFile(self._module)
        sys.stdout.write(confile.
                         functions[self._command['function']].
                         help)
        
    @property
    def _module(self):
        return __import__(self._command['filename'].
                          replace('.py', ''))
        
    @property
    def _arguments(self):
        arguments = []
        for argument in self._command['arguments']:
            (name, value,) = self._split_argument(argument)            
            value = self._represent_argument_value(value)
            arguments.append(self._join_argument(name, value))            
        return ', '.join(arguments)
    
    @staticmethod
    def _split_argument(argument):
        splited = argument.split('=', 1)
        if len(splited) == 1:
            return (None, argument,)
        else:
            return splited
    
    @staticmethod
    def _represent_argument_value(value):
        try:
            #TODO: pass len([]) - fix?
            return str(eval(value, {}, {}))
        except Exception:
            return repr(value)

    @staticmethod        
    def _join_argument(name, value):
        if not name:
            return value                
        else:
            return '='.join([name, value])
                  
                
class ConnectorFile(object):
    
    def __init__(self, module):
        self.functions = {}
        for name in dir(module):
            obj = getattr(module, name)
            if (not name.startswith('_') and
                isinstance(obj, types.FunctionType) and                
                getattr(obj, '__module__', None) == module.__name__):
                self.functions[name] = ConnectorFunction(obj)
        
    @property
    def list(self):
        return '\n'.join(sorted(self.functions))+'\n'


class ConnectorFunction(object):
    
    def __init__(self, function):
        self._function = function
    
    @property
    def name(self):
        return self._function.func_name
    
    @property
    def help(self):
        return '\n'.join(self._signature+self._docstring)+'\n'

    @property
    def _signature(self):
        return [('{name}({argstring})'.
                 format(name=self.name,
                        argstring=self._argstring))]
    
    @property
    def _docstring(self):
        docstring = []
        getdoc = inspect.getdoc(self._function)
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
        return inspect.getargspec(self._function)

    
if __name__ == '__main__':
    main()           

import unittest

class ConnectorFileTest(unittest.TestCase):
    
    def setUp(self):
        self.confile = ConnectorFile(sys.modules[__name__])
        
    def test_list(self):
        self.assertEqual(self.confile.list, 'main\n')


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
            "function(a, b='default', *args, **kwargs)\ndocstring\n")

        
class ConnectorFunctionTest_empty_function(unittest.TestCase):
    
    def setUp(self):
        def empty():
            pass
        self.confunc = ConnectorFunction(empty)
    
    def test_name(self):
        self.assertEqual(self.confunc.name, 'empty') 
        
    def test_help(self):
        self.assertEqual(self.confunc.help, 'empty()\n')               