#!/usr/bin/env python
# coding: utf-8

import re
from setuptools import setup, find_packages


setup(
    name='dictmixin',
    __version__=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open('dictmixin/__init__.py').read()).group(1),
    description='Parsing mixin which converts `data class instance`, `dict object`, and `json string` each other.',
    license='MIT',
    author='tadashi-aikawa',
    author_email='syou.maman@gmail.com',
    maintainer='tadashi-aikawa',
    maintainer_email='tadashi-aikawa',
    url='https://github.com/tadashi-aikawa/dictmixin.git',
    keywords='dict json convert parse each other',
    packages=find_packages(exclude=['tests*']),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
    ],
)
