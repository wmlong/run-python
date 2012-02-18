import subprocess
from package import Package

def release(step='minor', level='final'):
    """
    Release package with version type and level.
    Types:
    - major
    - minor
    - micro
    """
    if test() == 0:
        commit()
        version(action='increase', step=step, level=level)
        commit(message='updated version')
        push(branch='develop')
        checkout(branch='master')
        merge(branch='develop')
        tag(name=version(action='return'))
        push(branch='master', tags=True)
        register()
        clean()
        checkout(branch='develop')
        
def test():
    """
    Test package.
    """
    command = ['nosetests']
    return subprocess.call(command)

def version(action='print', step='minor', level='final'):
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
    package = Package()
    if action == 'return':
        return package.version
    elif action == 'print':
        print(package.version)
    elif action == 'increase':        
        package.version = (package.version.
                           next(step=step, level=level))            

def register():
    """
    Register package.
    """
    command = ['sudo', 'python', 'setup.py', 
               'register', 'sdist', 'upload']
    return subprocess.call(command)

def clean():
    command = ['sudo', 'rm', '-rf', 
               'dist', 'build', '*.egg-info']
    return subprocess.call(' '.join(command), shell=True)
       
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