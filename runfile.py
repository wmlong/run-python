import sys
import fileinput
import subprocess
import run_python as package

def release(type='minor', level='final'):
    """
    Release package with version type and level.
    Types:
    - major
    - minor
    - micro
    """
    if test() == 0:
        commit()
        version(action='increase', type=type, level=level)
        commit(message='updated version')
        push(branch='develop')
        checkout(branch='master')
        merge(branch='develop')
        tag(name=version(action='return'))
        push(branch='master', tags=True)
        register()
        checkout(branch='develop')
        
def test():
    """
    Test package.
    """
    command = ['nosetests']
    return subprocess.call(command)

def version(action='print', type='minor', level='final'):
    """
    Print or increase with type and level package version.   
    Actions:
    - print
    - increase
    Types:
    - major
    - minor
    - micro
    """
    version = package.__version__
    if action == 'return':
        return version    
    elif action == 'print':
        print(version)
    elif action == 'increase':
        module = sys.modules[version.__module__]
        source = module. __file__.replace('.pyc', '.py')
        for line in fileinput.input(source, inplace=True):
            if line.strip().startswith(type.upper()):
                current = getattr(package.__version__, type.upper())     
                line = line.replace(str(current), str(current+1))
            if line.strip().startswith('RELEASELEVEL'):
                line = line.replace(version.RELEASELEVEL, level)
            sys.stdout.write(line)
        reload(module)
        reload(package)

def register():
    """
    Register package.
    """
    command = ['sudo', 'python', 'setup.py', 'register', 'sdist', 'upload']
    return subprocess.call(command)

def commit(message=None):
    """
    Commit changes with message.
    """
    command = ['git', 'commit', '-a']
    if message:
        command.append('-m')
        command.append(message)
    subprocess.call(command)
    
def tag(name):
    """
    Add tag name.
    """
    command = ['git', 'tag', name]
    subprocess.call(command)
    
def checkout(branch):
    """
    Checkout branch.
    """
    command = ['git', 'checkout', branch]
    subprocess.call(command)
    
def merge(branch):
    """
    Merge branch.
    """
    command = ['git', 'merge', branch]
    subprocess.call(command)
    
def push(branch, tags=False):
    """
    Push branch to origin.
    """
    command = ['git', 'push', 'origin', branch]
    if tags:
        command.append('--tags')
    subprocess.call(command)