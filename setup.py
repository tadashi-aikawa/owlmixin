#!/usr/bin/env python
# coding: utf-8

from setuptools import setup, find_packages

setup(
    name='dictmixin',
    version='0.1.0',
    description='Parsing mixin which converts `data class instance`, `dict object`, and `json string` each other.',
    license='MIT',
    author='Tadashi Aikawa',
    author_email='syou.maman@gmail.com',
    url='https://github.com/tadashi-aikawa/dictmixin.git',
    keywords='dict json convert parse each other',
    packages=find_packages(),
    install_requires=[]
)
