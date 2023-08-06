from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='sgdatadog',
  version='0.0.1',
  description='AI powered by SGDATADOG',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Mr LIU',
  author_email='l1813379886@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='sgdatadog', 
  packages=find_packages(),
  install_requires=[''] 
)