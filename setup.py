#!/usr/bin/env python
from setuptools import setup, find_packages
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='HogeScraper',
    version='0.1',
    description='Python module to scrape Hogecoin data',
    long_description=read('README.md'),
    url='https://github.com/Durendal/HogeScraper',
    py_modules=['hogescraper'],
    zip_safe=False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
)