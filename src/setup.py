#!/usr/bin/env python3

from setuptools import setup, find_packages

import pomo2ebas as pomo2ebas

setup(
    name='pomo2ebas',
    packages=find_packages(where="."),
    package_dir={"pomo2ebas": "./pomo2ebas"},
    install_requires=[
       "pyyaml==6.0.1"
    ],
    tests_require=[],
    version=pomo2ebas.__version__,
    description='',
    download_url='',
    long_description="""A library to transform POMO data to EBAS data.""",
    platforms='OS Independent',
    classifiers=[],
)