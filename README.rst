=========
dictmixin
=========

|travis| |coverage| |complexity| |versions| |license|

Parsing mixin which converts ``data class instance``, ``dict object``, ``json string`` and ``yaml string`` each other.


Installation
============

.. code-block::

    pip install dictmixin


API
===

**From instance to another**

- ``to_dict``
    - instance => dict
- ``to_json``
    - instance => json string
- ``to_pretty_json``
    - instance => json string (has indent and line break)
- ``to_yaml``
    - instance => yaml string

**From something to instance**

- ``from_dict``
    - dict => instance [1]_
- ``from_dict2list``
    - dict => List[instance] [1]_
- ``from_dict2dict``
    - dict => Dict[instance] [1]_
- ``from_json``
    - json string => instance
- ``from_yaml``
    - yaml string => instance


.. [1] Also includes optional methods. (``from_optional_xxx``)


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
