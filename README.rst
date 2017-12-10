========
OwlMixin
========

|pypi| |travis| |coverage| |complexity| |versions| |license|

Mixin which converts ``data class instance`` and others each other more simple.

-- :warning: **Attention** :warning: --
 
Please migrate from 1.x to 2.x

* ``OwlMixin >= 2.0.0`` support python 3.6 and upper only.
* ``OwlMixin >= 2.0.0`` has many breaking changes for many improvements.
* ``OwlMixin >= 2.0.0`` documentation site has not completed yet (but you can trust pydoc always!)
* ``OwlMixin < 2.0.0`` has **vulnerability** fixed only ``OwlMixin >= 2.0.0a12``.

Motivation
==========

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following ``Example`` and ``API Reference`` sections.


Installation
============

.. code-block:: bash

    pip install owlmixin


API Reference
=============

https://tadashi-aikawa.github.io/owlmixin/


Example
=======

.. code-block:: python

    from owlmixin import OwlMixin
    from owlmixin.owlenum import OwlEnum
    from owlmixin.owloption import TOption
    from owlmixin.owlcollections import TList

    class Color(OwlEnum):
        RED = "red"
        GREEN = "green"
        BLUE = "blue"

    class Food(OwlMixin):
        id: int
        name: str
        color: TOption[Color]

    class Human(OwlMixin):
        id: int
        name: str
        favorite: TList[Food]

    jiro = Human.from_dict({
        "id": 10,
        "name": "jiro",
        "favorite": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "orange", "color": "green"}
        ]
    })

    >>> jiro.id
    10
    >>> jiro.name
    'jiro'

    >>> print(jiro.to_dict())
    {'id': 10, 'name': 'jiro', 'favorite': [{'id': 1, 'name': 'apple'}, {'id': 2, 'name': 'orange', 'color': 'green'}]}

    >>> print(jiro.favorite[0].to_pretty_json())
    {
        "id": 1,
        "name": "apple"
    }

    >>> print(jiro.to_yaml())
    favorite:
      - id: 1
        name: apple
      - color: green
        id: 2
        name: orange
    id: 10
    name: jiro

    >>> print(jiro.favorite.to_csv(['id', 'name', 'color'], with_header=True))
    id,name,color
    1,apple,
    2,orange,green


You can also use methods chains as following.

.. note::

    Below sample code uses `kachayev/fn.py <https://github.com/kachayev/fn.py>`_, great package!!


.. code-block:: python

    >>> from owlmixin.owloption import TOption
    >>> from owlmixin.owlcollections import TList
    >>>
    >>> from fn import _
    >>>
    >>>
    >>> class Repository(OwlMixin):
    ...     id: int
    ...     name: str
    ...     description: TOption[str]
    ...     stargazers_count: int
    ...
    >>>
    >>> class GithubRepository(OwlMixin):
    ...     total_count: int
    ...     incomplete_results: bool
    ...     items: TList[Repository]
    ...
    >>>
    >>> print(
    ...     GithubRepository \
    ...         .from_json_url("https://api.github.com/search/repositories?q=git") \
    ...         .items \
    ...         .filter(_.stargazers_count > 100) \
    ...         .order_by(_.stargazers_count, True) \
    ...         .head(5) \
    ...         .emap(lambda v, i: {
    ...             'RANK': i+1,
    ...             'STAR': v.stargazers_count,
    ...             'NAME': v.name,
    ...             'DESCRIPTION': v.description
    ...         }) \
    ...         .to_csv(fieldnames=["RANK", "STAR", "NAME", "DESCRIPTION"], with_header=True)
    ... )

    RANK,STAR,NAME,DESCRIPTION
    1,50787,gitignore,A collection of useful .gitignore templates
    2,19308,gogs,Gogs is a painless self-hosted Git service.
    3,17750,git,Git Source Code Mirror - This is a publish-only repository and all pull requests are ignored. Please follow Documentation/SubmittingPatches procedure for any of your improvements.
    4,10744,hub,hub helps you win at git.
    5,10338,tips,Most commonly used git tips and tricks.

Don't you think smart?


For developer
============

Release
-------

0. `make test doctest`
1. Increments version in __init__.py
2. `make package-docs`
3. `git commit -av` with message ':package: Versino $(version)'
4. `git tag $(version) -m $(version)`
5. `make release` which means uploading PyPI!
6. Install new version and confirm
7. Make PR, $(version) => master
8. Merge PR


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
