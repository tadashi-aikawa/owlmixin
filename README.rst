========
owlmixin
========

|pypi| |docslatest| |travis| |coverage| |complexity| |versions| |license|

Mixin which converts ``data class instance`` and others each other more simple.


Motivation
==========

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following ``Example`` and ``API Reference`` sections.


Installation
============

.. code-block:: bash

    pip install owlmixin


Example
=======

| You don't need to use ``typing`` necessarily, but I recommend to use this to make your codes more robust.
| See `PEP 484 -- Type Hints <https://www.python.org/dev/peps/pep-0484/>`_.

.. warning::

    If you use python 3.5.0 or 3.5.1, please use ``# type: str`` instead of ``# type: Text``

.. code-block:: python

    from typing import Text, Optional
    from owlmixin import OwlMixin
    from owlmixin.owlcollections import TList

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
    >>> print(jiro.to_dict())
    {'favorite': [{'color': None, 'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}
    >>> print(jiro.to_dict(ignore_none=False))
    {'favorite': [{'id': 1, 'name': 'apple'}, {'color': 'white', 'id': 2, 'name': 'orange'}], 'id': 10, 'name': 'jiro'}


You can also use methods chains as following.

.. code-block:: python

    from typing import Optional
    from owlmixin import OwlMixin
    from owlmixin.owlcollections import TList

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


API Reference
=============

* |docslatest| for master
* |docs| for current stable version


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
.. |docs| image:: https://readthedocs.org/projects/owlmixin/badge/?version=stable
    :target: http://owlmixin.readthedocs.io/en/stable/api.html?badge=stable
    :alt: Documentation Status
.. |docslatest| image:: https://readthedocs.org/projects/owlmixin/badge/?version=latest
    :target: http://owlmixin.readthedocs.io/en/latest/api.html?badge=latest
    :alt: Documentation Status
.. |versions| image:: https://img.shields.io/pypi/pyversions/owlmixin.svg
.. |license| image:: https://img.shields.io/github/license/mashape/apistatus.svg
