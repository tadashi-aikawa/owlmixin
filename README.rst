========
owlmixin
========

|pypi| |travis| |coverage| |complexity| |versions| |license|

Parsing mixin which converts ``data class instance``, ``dict object``, ``json string`` and ``yaml string`` each other.


Motivation
==========

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following ``Example`` and ``API`` sections.


Example
=======

You don't need to use ``typing`` necessarily, but I recommend to use this to make your codes more robust.
See `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_.

.. code-block:: python

    from typing import Text, Optional
    from owlmixin import OwlMixin

    class Food(OwlMixin):
        def __init__(self, id, name, color=None):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.color = color  # type: Optional[Text]

    class Human(OwlMixin):
        def __init__(self, id, name, favorite):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.favorite = Food.from_dict2list(favorite)  # type: TList[Food]

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
    - TDict[instance] => dict
- ``to_dicts``
    - TList[instance] => List[dict]
- ``to_json``
    - instance => json string
- ``to_pretty_json``
    - instance => json string (has indent and line break)
- ``to_yaml``
    - instance => yaml string

**From something to instance**

- ``from_dict`` [1]_ [2]_
    - dict => instance
- ``from_optional_dict`` [1]_ [2]_
    - Optional[dict] => Optional[instance]
- ``from_dicts`` [1]_ [2]_
    - dict => TList[instance]
- ``from_optional_dicts`` [1]_ [2]_
    - Optional[dict] => Optional[instance]
- ``from_dicts_by_key`` [1]_ [2]_
    - dict => TDict[instance]
- ``from_optional_dicts_by_key`` [1]_ [2]_
    - Optional[dict] => Optional[instance]
- ``from_json`` [1]_ [2]_
    - json string => instance
- ``from_json_url`` [1]_ [2]_
    - url (which returns json) => instance
- ``from_yaml`` [1]_ [2]_
    - yaml string or file => instance
- ``from_csv`` [1]_ [2]_
    - csv file => TList[instance]


.. [1] Keys are transformed to snake case in order to compliant PEP8. (set ``force_snake_case=False`` if you don't want to do it.)
.. [2] Key ``self`` is transformed to ``_self`` in order to avoid duplicate.


Installation
============

.. code-block::

    pip install owlmixin


.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/owlmixin.svg?branch=master
    :target: https://api.travis-ci.org/tadashi-aikawa/owlmixin
    :alt: Build Status
.. |coverage| image:: https://codeclimate.com/github/tadashi-aikawa/owlmixin/badges/coverage.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/owlmixin/coverage
    :alt: Test Coverage
.. |complexity| image:: https://codeclimate.com/github/tadashi-aikawa/owlmixin/badges/gpa.svg
    :target: https://codeclimate.com/github/tadashi-aikawa/owlmixin
    :alt: Code Climate
.. |pypi| image::   https://img.shields.io/pypi/v/owlmixin.svg
.. |versions| image:: https://img.shields.io/pypi/pyversions/owlmixin.svg
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
