import os
import imp
from setuptools import find_packages

class Package(dict):
    
    #Maindata
    NAME = 'run-python'
    PACKAGE_DATA={         
        '': ['files/*'],
    }
    INSTALL_REQUIRES = ['run-core']
    TEST_SUITE = 'nose.collector'
    TESTS_REQUIRE = ['nose']
    
    #Metadata
    DESCRIPTION = 'Python driver for Run'
    AUTHOR = 'Respect31'
    AUTHOR_EMAIL='team@respect31.com'
    MAINTAINER='Respect31'
    MAINTAINER_EMAIL='team@respect31.com'
    URL='https://github.com/respect31/run-python'
    PLATFORMS=['Unix', 'POSIX']
    LICENSE='MIT license'     
    CLASSIFIERS=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',             
    ]

    def __init__(self):
        self.update([(name.lower(), getattr(self, name)) 
                     for name in Package.__dict__
                     if not name.startswith('_')])    
        
    @property
    def version(self):
        path = os.path.join(os.path.dirname(__file__), 'run_python')        
        meta = imp.find_module('version', [path])
        module = imp.load_module('version', *meta)
        meta[0].close()
        return module.Version()
    
    @version.setter
    def version(self, version):
        code = version.code
        with open(self.version.path, 'w') as f:
            f.write(code)

    @property
    def packages(self):
        return find_packages(exclude=['tests*'])
    
    @property
    def long_description(self):
        with open('README.rst') as f:
            return f.read()
    
    @property    
    def download_url(self):
        return ('https://github.com/respect31/run-python/tarball/{version}'.
                format(version=self.version))