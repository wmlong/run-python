from setuptools import setup, find_packages
from run import VERSION

setup(name='run-python',
      version=VERSION,
      description='Run Python',
      author='Respect31',
      author_email='team@respect31.com',
      maintainer='roll',
      maintainer_email='roll@respect31.com',
      url='https://github.com/respect31/run-python',
      download_url='https://github.com/respect31/run-python/tarball/develop',
      packages=find_packages(exclude=['tests*']),
      package_data={
          'run_python': ['files/*'],
      },    
      classifiers=[],)