"""setup.py -- Package and distributions management."""
from setuptools import setup, find_packages

with open('README.md') as f:
    README = f.read()

with open('LICENSE.md') as f:
    LICENSE = f.read()

setup(
    name='Team - Example Module'
    , version='2020.4.2'
    , description='Modules for Team'
    , long_description=README
    , author='Joel E Carlson'
    , author_email='joel.elmer.carlson@gmail.com'
    , url='https://github.com/joelelmercarlson/coding'
    , license=LICENSE,
    packages=find_packages(exclude=('tests', 'docs'))
)
