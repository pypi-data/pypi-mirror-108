import codecs
import os
import re
from setuptools import setup

def local_file(file):
  return codecs.open(
    os.path.join(os.path.dirname(__file__), file), 'r', 'utf-8'
)

install_reqs = [
  line.strip()
  for line in local_file('requirements.txt').readlines()
  if line.strip() != ''
]

setup(
    name='VizKG',
    packages=['VizKG', 'VizKG.charts', 'VizKG.utils'],
    version='0.0.0.1',
    description='Visualization library for SPARQL query results',
    author='Hana',
    install_requires=install_reqs,
    license='MIT',
)