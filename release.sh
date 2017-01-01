#!/usr/bin/env bash

readonly RELEASE_VERSION=$1
readonly PYPI_PASSWORD=$2

python setup.py bdist_wheel
twine upload dist/dictmixin-${RELEASE_VERSION}-py2.py3-none-any.whl -P ${PYPI_PASSWORD}
