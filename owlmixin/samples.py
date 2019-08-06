# coding: utf-8

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TDict, TList
from owlmixin.owlenum import OwlEnum, OwlObjectEnum


class Animal(OwlObjectEnum):  # pragma: no cover
    DOG = ("dog", {"cry": "bow-wow"})
    CAT = ("cat", {"cry": "mewing"})

    def cry(self):
        return self.object["cry"]


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
    language: str = "japanese"
