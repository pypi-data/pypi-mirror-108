from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='torch_airflow_sdk',
  version='0.0.12',
  description='test pkg',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',
  author='vaishvik24',
  author_email='vaishvik@acceldata.io',
  license='MIT',
  classifiers=classifiers,
  keywords='python',
  packages=find_packages(),
  install_requires=['requests', 'dataclasses', 'typing', 'torch_sdk']
)