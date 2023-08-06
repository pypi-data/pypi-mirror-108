from setuptools import find_packages, setup

# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Toncalculator',
  version='0.0.5',
  description='A basic calculator',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  # the URL of your package's home page e.g. github link
  author='Mahmudul Hahan Tonmoy',
  author_email='playerandgamertonmoy@gmail.com',
  license='MIT', # note the American spelling
  classifiers=classifiers,
  keywords='calculator, toncalculator, add, addison, subdivision, log, sin, cos, tan, coat, sce, cosec, a simple calculator, fine calculator, terminal calculator', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=[''] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)
