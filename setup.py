#!/usr/bin/env python
from setuptools import setup, find_packages
import os

LIB_NAME    = 'hogescraper'
DESCRIPTION = 'Python module to scrape Hogecoin data'
VERSION     = '0.0.2'
AUTHOR      = 'Durendal'
EMAIL       = 'durendal@durendals-domain.com'
URL         = 'https://github.com/Durendal/HogeScraper'

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name=LIB_NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    download_url="%s.git" % URL,
    packages=find_packages(),
    zip_safe=False,
    install_requires=['web3', 'requests'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],
    python_requires=">=3.6",
)