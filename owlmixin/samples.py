# coding: utf-8

from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum, OwlObjectEnum
from owlmixin import OwlMixin, TOption


class Animal(OwlObjectEnum):  # pragma: no cover
    DOG = ("dog", {"cry": "bow-wow"})
    CAT = ("cat", {"cry": "mewing"})

    def crow(self):
        return self.object


class Color(OwlEnum):  # pragma: no cover
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class Food(OwlMixin):  # pragma: no cover
    name: str
    names_by_lang: TOption[TDict[str]]


class Human(OwlMixin):  # pragma: no cover
    id: int
    name: str
    favorites: TList[Food]


class Machine(OwlMixin):  # pragma: no cover
    id: int
    name: str


class Japanese(OwlMixin):  # pragma: no cover
    name: str
    language: str = 'japanese'
