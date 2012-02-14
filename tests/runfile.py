import sys
import subprocess

def function_normal(a, b='default', *args, **kwargs):
    """
    docstring
    """
    sys.stdout.write('function_normal:'+a+','+b)
    subprocess.call(['pwd'])
    
def function_empty():
    pass 