from setuptools import setup, find_packages
# See note below for more information about classifiers
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: Apache Software License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='jesviiBasicCalculator', #modeule name
  version='0.0.1',
  description='A basic calculator with addition, subtraction, multiplication and division of two numbers',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  #url='',  # the URL of your package's home page e.g. github link
  author='jes',
  author_email='thejes106@gmail.com',
  license='Apache', # note the American spelling
  classifiers=classifiers,
  keywords='calculator', # used when people are searching for a module, keywords separated with a space
  packages=find_packages(),
  install_requires=['numpy'] # a list of other Python modules which this module depends on.  For example RPi.GPIO
)