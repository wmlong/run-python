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
        version(action='increase', type='minor', level='final')
        commit('release')
        tag(version())

def test():
    """
    Test package.
    """
    return subprocess.call('nosetests', shell=True)

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
    if action == 'print':
        print(package.__version__)
    elif action == 'increase':
        for line in fileinput.input('run/version.py', inplace=True):
            if line.strip().startswith(type.upper()):
                current = getattr(package.__version__, type.upper())     
                line = line.replace(str(current), str(current+1))
            if line.strip().startswith('RELEASELEVEL'):
                line = line.replace(package.__version__.RELEASELEVEL, level)
            sys.stdout.write(line)
        reload(package)
        
def commit(message):
    """
    Commit changes with message.
    """
    subprocess.call(['git commit -am "{message}"'.
                     format(message=message)], shell=True)
    
def tag(name):
    """
    Add tag name.
    """
    subprocess.call(['git tag {name}'.
                     format(name=name)], shell=True)   