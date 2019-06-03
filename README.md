OwlMixin
========

[![travis](https://api.travis-ci.org/tadashi-aikawa/owlmixin.svg?branch=master)](https://travis-ci.org/tadashi-aikawa/owlmixin/builds)
[![coverage](https://codeclimate.com/github/tadashi-aikawa/owlmixin/badges/coverage.svg)](https://codeclimate.com/github/tadashi-aikawa/owlmixin/coverage)
[![complexity](https://codeclimate.com/github/tadashi-aikawa/owlmixin/badges/gpa.svg)](https://codeclimate.com/github/tadashi-aikawa/owlmixin)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()
[![pypi](https://img.shields.io/pypi/v/owlmixin.svg)](https://pypi.org/project/owlmixin/)
[![versions](https://img.shields.io/pypi/pyversions/owlmixin.svg)]()

**(ﾟ∀ﾟ) v4.0 have ??? breaking changes**

* `OwlMixin`
  * Must use keyword arguments in `from_XXX` and `to_XXX` except for some ones
  * `from_csvf` -> `from_csvf_to_list`
* `TList`
  * `head` -> `take`
  * `partial` -> `partition` (switch left and right)
* `transformers.XXX`
  * Must use keyword arguments in
    * `to_dict`
    * `to_dicts`
    * `to_json`
    * `to_jsonf`
    * `to_yaml`
    * `to_yamlf`
    * `to_csv`
    * `to_csvf`


Motivation
----------

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following `Example` and `API Reference` sections.


Installation
------------

```
$ pip install owlmixin
```


API Reference
-------------

https://tadashi-aikawa.github.io/owlmixin/


Example
-------

```python
from owlmixin import OwlMixin, OwlEnum, TOption, TList

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
```

Then...

```
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
```

You can also use methods chains as following.

> Below sample code uses [kachayev/fn.py](https://github.com/kachayev/fn.py), great package!!


```python
from owlmixin import OwlMixin, TOption, TIterator

from fn import _


class Repository(OwlMixin):
    id: int
    name: str
    description: TOption[str]
    stargazers_count: int


class GithubRepository(OwlMixin):
    total_count: int
    incomplete_results: bool
    items: TIterator[Repository]
```

Then...

```python
>>> print(
...     GithubRepository
...         .from_json_url("https://api.github.com/search/repositories?q=git")
...         .items
...         .filter(_.stargazers_count > 100)
...         .order_by(_.stargazers_count, True)
...         .take(5)
...         .emap(lambda v, i: {
...             'RANK': i+1,
...             'STAR': v.stargazers_count,
...             'NAME': v.name,
...             'DESCRIPTION': v.description
...         })
...         .to_csv(fieldnames=["RANK", "STAR", "NAME", "DESCRIPTION"], with_header=True)
... )
RANK,STAR,NAME,DESCRIPTION
1,84643,gitignore,A collection of useful .gitignore templates
2,30456,gogs,Gogs is a painless self-hosted Git service.
3,29908,git-flight-rules,Flight rules for git
4,27704,git,Git Source Code Mirror - This is a publish-only repository and all pull requests are ignored. Please follow Documentation/SubmittingPatches procedure for any of your improvements.
5,15541,tips,Most commonly used git tips and tricks.
```

Don't you think smart?


For developer
------------

Requires pipenv and make.


### Commands

```
# Create env
$ make init

# Build documentation and run server locally
$ make serve-docs
```


### Version up

Before release, you need to

1. Confirm that your branch name equals release version

Then

```
$ make release
```


