#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from dictmixin import __author__, __version__, __license__

setup(
    name='dictmixin',
    version=__version__,
    description='Parsing mixin which converts `data class instance`, `dict object`, and `json string` each other.',
    license=__license__,
    author=__author__,
    author_email='syou.maman@gmail.com',
    url='https://github.com/tadashi-aikawa/dictmixin.git',
    keywords='dict json convert parse each other',
    packages=find_packages(),
    install_requires=[],
)
