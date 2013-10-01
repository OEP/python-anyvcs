import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

execfile('anyvcs/__init__.py')

setup(
  name='anyvcs',
  version=__version__,
  packages=['anyvcs'],
  include_package_data=True,
  license='GNU Lesser General Public License v3 (LGPLv3)',
  description='An abstraction layer for multiple version control systems.',
  long_description=README,
  url='https://github.com/ScottDuckworth/python-anyvcs',
  author='Scott Duckworth',
  author_email='sduckwo@clemson.edu',
  classifiers=[
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Software Development :: Version Control',
  ],
)