from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='xiaoweiahfang',
  version='0.0.3',
  description='I am Xiao Wei or Ah Fang',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='david shem',
  author_email='tpython111@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='xiaoweiahfang', 
  packages=find_packages(),
  install_requires=[''] 
)
