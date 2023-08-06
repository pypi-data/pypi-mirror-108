from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='textwriter',
  version='0.0.2',
  description='A basic text writer',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Joaf',
  author_email='admin@jfncgamerinc.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='textwriter', 
  packages=find_packages(),
  install_requires=[''] 
)
