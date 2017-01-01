#!/usr/bin/env bash

python setup.py bdist_wheel
twine upload dist/dictmixin-${RELEASE_VERSION}-py2.py3-none-any.whl \
  --repository-url "https://pypi.python.org/pypi" \
  -u tadashi-aikawa \
  -p ${PYPI_PASSWORD}
