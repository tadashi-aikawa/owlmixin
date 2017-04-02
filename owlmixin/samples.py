# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import Optional
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum, OwlObjectEnum
from owlmixin import OwlMixin


class Animal(OwlObjectEnum):  # pragma: no cover
    DOG = ("dog", "bow-wow")
    CAT = ("cat", "mewing")

    def crow(self):
        return self.object


class Color(OwlEnum):  # pragma: no cover
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Food(OwlMixin):  # pragma: no cover
    def __init__(self, name, names_by_lang=None, **extra):
        self.name = name  # type: unicode
        self.names_by_lang = names_by_lang  # type: Optional[TDict[unicode, unicode]]


class Human(OwlMixin):  # pragma: no cover
    def __init__(self, id, name, favorites):
        self.id = id  # type: int
        self.name = name  # type: unicode
        self.favorites = Food.from_dicts(favorites)  # type: TList[Food]


class Machine(OwlMixin):  # pragma: no cover
    def __init__(self, id, name):
        self.id = id  # type: int
        self.name = name  # type: unicode
