# OwlMixin

[![pypi](https://img.shields.io/pypi/v/owlmixin.svg)](https://pypi.org/project/owlmixin/)
[![versions](https://img.shields.io/pypi/pyversions/owlmixin.svg)](https://pypi.org/project/owlmixin/)
[![Actions Status](https://github.com/tadashi-aikawa/owlmixin/workflows/Tests/badge.svg)](https://github.com/tadashi-aikawa/owlmixin/actions)
[![codecov](https://codecov.io/gh/tadashi-aikawa/owlmixin/branch/master/graph/badge.svg)](https://codecov.io/gh/tadashi-aikawa/owlmixin)
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()


<details>
    <summary><b>(ﾟ∀ﾟ) v5.0 have breaking changes</b></summary>
    <div>

* `TIterator#group_by`
  * Return `TDict[TList[T]]` instead of `TDict[TIterator[T]]`
    </div>
</details>

<details>
    <summary><b>(ﾟ∀ﾟ) v4.0 have breaking changes</b></summary>
    <div>

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
    </div>
</details>


## 💪 Motivation

Have you ever wanted to write robust code in Python? This library will make such your wishes come true.

Define your data class which is extend OwlMixin, you can use some useful methods which help your codes robust.
See following `Example` and `API Reference` sections.


## 💃 Installation

```bash
pip install owlmixin
```


## 📜 API Reference

https://tadashi-aikawa.github.io/owlmixin/


## 👉 Examples

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

```python
from owlmixin import OwlMixin, TOption, TIterator


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
...         .filter(lambda x: x.stargazers_count > 100)
...         .order_by(lambda x: x.stargazers_count, True)
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


## 💻 For developers

### Requirements

* uv
* make

### Flow

1. Development on master and if you need branches and issues, create them
2. Use the [Conventional Commits] message

### Commands

```bash
# Create env
$ uv run

# Build documentation and run server locally
$ make serve-docs

# Test (Doc test & Unit test)
$ make test
```


## 📦 Release

https://github.com/tadashi-aikawa/owlmixin/actions/workflows/release.yaml?query=workflow%3ARelease

### (Appendix) Another way

If you can't or don't want to use GitHub Actions, you can release locally as following.

#### (a1) Requirements

* **Windows is not supported!!!**
* uv (with pypi authentications)
* make

#### (a2) Commands

```bash
make release version=x.y.z
```


[ghr]: https://github.com/tcnksm/ghr
[Conventional Commits]: https://www.conventionalcommits.org/ja/v1.0.0/
