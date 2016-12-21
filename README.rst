=========
dictmixin
=========

|pypi| |travis| |coverage| |complexity| |versions| |license|

Parsing mixin which converts ``data class instance``, ``dict object``, ``json string`` and ``yaml string`` each other.


Motivation
==========

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend DictMixin, you can use some useful methods which help your codes robust.
See following ``Example`` and ``API`` sections.


Example
=======

You don't need to use ``typing`` necessarily, but I recommend to use this to make your codes more robust.
See `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_.

.. code-block:: python

    from typing import Text, Optional
    from dictmixin import DictMixin

    class Food(DictMixin):
        def __init__(self, id, name, color=None):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.color = color  # type: Optional[Text]

    class Human(DictMixin):
        def __init__(self, id, name, favorite):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.favorite = Food.from_dict2list(favorite)  # type: List[Food]

    jiro = Human.from_dict({
        "id": 10,
        "name": "jiro",
        "favorite": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "orange", "color": "white"}
        ]
    })

    >>> jiro.id
    10
    >>> jiro.name
    'jiro'
    >>> print(jiro.favorite[0].to_pretty_json())
    {
        "color": null,
        "id": 1,
        "name": "apple"
    }
    >>> print(jiro.to_dict())
    {'favorite': [{'color': None, 'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}
    >>> print(jiro.to_dict(ignore_none=True))
    {'favorite': [{'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}


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


Installation
============

.. code-block::

    pip install dictmixin


.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/dictmixin.svg?branch=master
    :target: https://api.travis-ci.org/tadashi-aikawa/dictmixin
    :alt: Build Status
.. |coverage| image:: https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/coverage.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/dictmixin/coverage
    :alt: Test Coverage
.. |complexity| image:: https://codeclimate.com/github/tadashi-aikawa/dictmixin/badges/gpa.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/dictmixin
    :alt: Code Climate
.. |pypi| image:: 	https://img.shields.io/pypi/v/dictmixin.svg
.. |versions| image:: https://img.shields.io/pypi/pyversions/dictmixin.svg
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
