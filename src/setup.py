#!/usr/bin/env python3

from setuptools import setup, find_packages

import pomo2ebas as pomo2ebas

setup(
    name='pomo2ebas',
    packages=find_packages(where="."),
    package_dir={"pomo2ebas": "./pomo2ebas"},
    install_requires=[
       "pyyaml==6.0.1",
       "pytz==2023.3.post1"
       "dateutil==2.8.2"
    ],
    tests_require=[],
    version=pomo2ebas.__version__,
    description='',
    download_url='',
    long_description="""A library to transform POMO data to EBAS data.""",
    platforms='OS Independent',
    classifiers=[],
)