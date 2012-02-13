from setuptools import setup, find_packages
from run_python import VERSION

setup(#Data
      name='run-python',
      version=VERSION,
      packages=find_packages(exclude=['tests*']),
      package_data={
          'run_python': ['files/*'],
      },      
      install_requires=['run_core'],
      test_suite='nose.collector',
      tests_require=['nose'],
      
      #Metadata      
      description='Run Python',
      author='Respect31',
      author_email='team@respect31.com',
      maintainer='Respect31',
      maintainer_email='team@respect31.com',
      url='https://github.com/respect31/run-python',
      download_url='https://github.com/respect31/run-python/tarball/develop',
      license='Apache 2.0',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: Apache Software License',
          'Operating System :: Unix',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: System :: Systems Administration',
          'Topic :: Utilities',  
      ],)