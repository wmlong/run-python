import sys

#Test imports
import subprocess
from fixtures import Process
subprocess, Process

def function_normal(a, b='default', *args, **kwargs):
    """
    docstring
    """
    sys.stdout.write('function_normal: {a}, {b}'.format(a=a, b=b))
    
def function_empty():
    pass


class ClassToRun(object):
    
    def function(self):
        pass