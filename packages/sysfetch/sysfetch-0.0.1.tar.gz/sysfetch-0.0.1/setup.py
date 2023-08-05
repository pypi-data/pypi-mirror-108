import setuptools

import os
from os import path
from setuptools import setup

basedir = path.abspath(path.dirname(__file__))
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setuptools.setup(
    name='sysfetch',  
    version='0.0.1',
    scripts=['print-this.py'],
    author="Nandydark",
    description="Fetch system info!",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/nandydark/sysfetch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Freely Distributable",
        "Operating System :: OS Independent",
    ],
) 
