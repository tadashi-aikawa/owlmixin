#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages
from jsonmixin import __author__, __version__, __license__

setup(
    name='jsonmixin',
    version=__version__,
    description='Parsing mixin which converts `data class instance`, `dict object`, and `json string` each other.',
    license=__license__,
    author=__author__,
    author_email='syou.maman@gmail.com',
    url='https://github.com/tadashi-aikawa/json-mixin.git',
    keywords='json dict convert parse each other',
    packages=find_packages(),
    install_requires=[],
)
