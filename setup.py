#!/usr/bin/env python
# coding: utf-8

import os
import re
from setuptools import setup, find_packages

from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

here = os.path.abspath(os.path.dirname(__file__))


pfile = Project(chdir=False).parsed_pipfile
requirements = convert_deps_to_pip(pfile['packages'], r=False)
test_requirements = convert_deps_to_pip(pfile['dev-packages'], r=False)


def load_readme():
    with open(os.path.join(here, 'README.md')) as f:
        return f.read()


setup(
    name='owlmixin',
    version=re.search(
        r'__version__\s*=\s*[\'"]([^\'"]*)[\'"]',  # It excludes inline comment too
        open('owlmixin/version.py').read()).group(1),
    description='Mixin which converts ``data class instance`` and others each other more simple.',
    long_description=load_readme(),
    long_description_content_type=”text/markdown”,
    license='MIT',
    author='tadashi-aikawa',
    author_email='syou.maman@gmail.com',
    maintainer='tadashi-aikawa',
    maintainer_email='syou.maman@gmail.com',
    url='https://github.com/tadashi-aikawa/owlmixin.git',
    keywords='data class mixin instance dict json yaml csv convert parse each other functional',
    packages=find_packages(exclude=['tests*']),
    install_requires=requirements,
    extras_require={'test': test_requirements},
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
