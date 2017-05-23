#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))


def load_readme():
    with open(os.path.join(here, 'README.rst')) as f:
        return f.read()


def load_required_modules():
    with open(os.path.join(here, "requirements.txt")) as f:
        return [line.strip() for line in f.readlines() if line.strip()]


setup(
    name='owlmixin',
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open('owlmixin/__init__.py').read()).group(1),
    description='Mixin which converts ``data class instance`` and others each other more simple.',
    long_description=load_readme(),
    license='MIT',
    author='tadashi-aikawa',
    author_email='syou.maman@gmail.com',
    maintainer='tadashi-aikawa',
    maintainer_email='tadashi-aikawa',
    url='https://github.com/tadashi-aikawa/owlmixin.git',
    keywords='data class mixin instance dict json yaml csv convert parse each other functional',
    packages=find_packages(exclude=['tests*']),
    install_requires=load_required_modules(),
    extras_require={
        'test': ['pytest', 'pytest-cov', 'mock']
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6'
    ],
)
