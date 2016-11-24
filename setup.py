#!/usr/bin/env python
# coding: utf-8

import re
from os import read

from setuptools import setup, find_packages


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='dictmixin',
    version=find_version("dictmixin", "__init__.py"),
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
