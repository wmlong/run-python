import sys

def function_normal(a, b='default', *args, **kwargs):
    """
    docstring
    """
    sys.stdout.write('function_normal:'+a+','+b)
    
def function_empty():
    pass 