# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='binance-bot',
    version='0.1.0',
    description='Binance Bot Trade',
    long_description=readme,
    author='Nguyen Doan Cuong',
    author_email='cuongnd86@gmail.com',
    url='https://google.com.vn',
    license=license,
    packages=find_packages(exclude=('tests', '_docs'))
)

