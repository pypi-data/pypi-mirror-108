from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='easy-stocks',
  version='1.0.1',
  description='making finance esayer for developpers',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Adam Maras',
  author_email='adam3.maras@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='stock',
  packages=find_packages(),
  install_requires=['requests'] 
)