import os
from setuptools import setup, find_packages
from pkg_resources import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

setup(
  name='inspireapi',
  version='0.0.2',
  url='https://github.com/carterjfulcher/inspireapi',
  author='carterjfulcher',
  author_email='fulcher.carter@gmail.com',
  packages=find_packages(exclude=("tests",)),
  install_reqs=[],
  platforms='any',
  license='MIT',
  ext_modules=[],
  description="Unofficial API for Inspire Investing's Insight API that provides Biblically responsible insights to securities",
  long_description='See https://github.com/carterjfulcher/inspireapi',
)
