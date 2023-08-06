from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='ymautomation',
  version='0.0.5',
  description='IoT',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://ymautomation.com',  
  author='YOGESHWARAN MURALIDHARAN ',
  author_email='ym@ymautomation.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='iot', 
  packages=find_packages(),
  install_requires=[''] 
)
