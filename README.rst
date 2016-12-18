dictmixin
=========

|travis| |coverage| |complexity| |versions| |license|

Parsing mixin which converts `data class instance`, `dict object`, `json string` and `yaml string` each other.


Installation
------------

.. code::

    pip install git+https://github.com/tadashi-aikawa/dictmixin@0.4.0


API
---

.. csv-table::
    :header: "from", "to", "method"
    :widths: 1,1,8

    "instance","dict","`to_dict`"
    "instance","json","`to_json`, `to_pretty_json`"
    "instance","yaml"    , "`to_yaml`"
    "dict",    "instance", "`from_dict`, `from_dict2list`, `from_dict2dict` [1]_"
    "dict",    "json"    , ""
    "dict",    "yaml"    , ""
    "json",    "instance", "`from_json`"
    "json",    "dict"    , ""
    "json",    "yaml"    , ""
    "yaml",    "instance", "`from_yaml`"
    "yaml",    "dict"    , ""
    "yaml",    "json"    , ""


.. [1] Also includes optional methods. (`from_optional_xxx`)

.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/dictmixin.svg?branch=master
    :target: https://api.travis-ci.org/tadashi-aikawa/dictmixin
    :alt: Build Status
.. |coverage| image:: https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/coverage.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/dictmixin/coverage
    :alt: Test Coverage
.. |complexity| image:: https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/gpa.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/dictmixin
    :alt: Code Climate
.. |versions| image:: https://img.shields.io/badge/python-2.7/3.3/3.4/3.5-blue.svg
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
