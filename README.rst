========
owlmixin
========

|pypi| |travis| |coverage| |complexity| |versions| |license|

Mixin which converts ``data class instance`` and others each other more simple.


Motivation
==========

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following ``Example`` and ``API`` sections.


Example
=======

You don't need to use ``typing`` necessarily, but I recommend to use this to make your codes more robust.
See `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_.

**WARNING: If you use python 3.5.0 or 3.5.1, please `# type: str` instead of `# type: Text`**

.. code-block:: python

    from typing import Text, Optional
    from owlmixin import OwlMixin, TList

    class Food(OwlMixin):
        def __init__(self, id, name, color=None):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.color = color  # type: Optional[Text]

    class Human(OwlMixin):
        def __init__(self, id, name, favorite):
            self.id = id  # type: Text
            self.name = name  # type: Text
            self.favorite = Food.from_dicts(favorite)  # type: TList[Food]

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
        "id": 1,
        "name": "apple"
    }
    >>> print(jiro.to_dict(ignore_none=False))
    {'favorite': [{'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}
    >>> print(jiro.to_dict())
    {'favorite': [{'color': None, 'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}


You can also use methods chains as following.

.. code-block:: python

    from typing import Optional
    from owlmixin import OwlMixin, TList

    # `**extra` is necessary to allow extra elements.
    # Note that you must define all properties in github response json if you don't use `**extra`
    class Repository(OwlMixin):
        def __init__(self, id, name, description, stargazers_count, **extra):
            self.id = id  # type: int
            self.name = name  # type: Text
            self.description = description  # type: Optional[Text]
            self.star_count = stargazers_count  # type: int

    class GithubRepository(OwlMixin):
        def __init__(self, total_count, incomplete_results, items):
            self.total_count = total_count  # type: int
            self.incomplete_results = incomplete_results  # type: bool
            self.repositories = Repository.from_dicts(items)  # type: TList[Repository]

    >>> r = GithubRepository \
    ...         .from_json_url("https://api.github.com/search/repositories?q=git") \
    ...         .repositories \
    ...         .filter(lambda x: x.star_count > 100) \
    ...         .order_by(lambda x: x.star_count, True) \
    ...         .map(lambda x: {
    ...             "id": x.id,
    ...             "message": '★{0.star_count}   {0.name}'.format(x)
    ...         }) \
    ...         .to_csv(fieldnames=["id", "message"], with_header=True)
    >>> print(r)
    id,message
    1062897,★45252   gitignore
    36502,★15888   git
    36560369,★2931   my-git
    18484639,★212   git


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
- ``to_csv``
    - TList[instance] => csv string

**From something to instance**

- ``from_dict`` [1]_ [2]_
    - dict => instance
- ``from_optional_dict`` [1]_ [2]_
    - Optional[dict] => Optional[instance]
- ``from_dicts`` [1]_ [2]_
    - List[dict] => TList[instance]
- ``from_optional_dicts`` [1]_ [2]_
    - Optional[List[dict]] => Optional[TList[instance]]
- ``from_dicts_by_key`` [1]_ [2]_
    - dict => TDict[instance]
- ``from_optional_dicts_by_key`` [1]_ [2]_
    - Optional[dict] => Optional[TDict[instance]]
- ``from_json`` [1]_ [2]_
    - json string => instance
- ``from_jsonf`` [1]_ [2]_ [3]_
    - json file path => instance
- ``from_json_to_list`` [1]_ [2]_
    - json string => TList[instance]
- ``from_jsonf_to_list`` [1]_ [2]_ [3]_
    - json file path => TList[instance]
- ``from_json_url`` [1]_ [2]_
    - url (which returns json) => instance
- ``from_yaml`` [1]_ [2]_
    - yaml string => instance
- ``from_yamlf`` [1]_ [2]_ [3]_
    - yaml file path => instance
- ``from_yaml_to_list`` [1]_ [2]_
    - yaml string => TList[instance]
- ``from_yamlf_to_list`` [1]_ [2]_ [3]_
    - yaml file path => TList[instance]
- ``from_csvf`` [1]_ [2]_ [3]_
    - csv file => TList[instance]


.. [1] Keys are transformed to snake case in order to compliant PEP8. (set ``force_snake_case=False`` if you don't want to do it.)
.. [2] Key ``self`` is transformed to ``_self`` in order to avoid duplicate.
.. [3] You can specify any encodings


Installation
============

.. code-block::

    pip install owlmixin


.. |travis| image:: https://api.travis-ci.org/tadashi-aikawa/owlmixin.svg?branch=master
    :target: https://travis-ci.org/tadashi-aikawa/owlmixin/builds
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
