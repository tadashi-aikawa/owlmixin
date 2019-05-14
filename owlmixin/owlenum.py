# coding: utf-8

import warnings
from enum import Enum
from typing import TypeVar

from debtcollector import removals

from owlmixin.transformers import ValueTransformer

T = TypeVar('T', bound='OwlObjectEnum')

warnings.simplefilter("once")


class OwlEnum(ValueTransformer, Enum):
    """ This class is similar to Enum except that can dump as json or yaml
    """

    @classmethod
    def from_value(cls, value: str):
        return cls(value)

    def to_value(self, ignore_none, force_value):
        return self.value


class OwlObjectEnum(ValueTransformer, Enum):
    """ This class is similar to OwlEnum except that can have additional object.

    Use case example:
        class Animal(OwlObjectEnum):
            DOG = ("dog", {"cry": "bow-wow"})
            CAT = ("cat", {"cry": "mewing"})

        def crow(self):
            return self.object["cry"]
    TODO: Not exec doctest
    """

    def __init__(self, symbol, obj):
        self.symbol = symbol
        self.object = obj

    @classmethod
    def from_value(cls, value: str) -> T:
        """Create instance from symbol
        :param value: unique symbol
        :return: This instance

        Usage:

            >>> from owlmixin.samples import Animal
            >>> Animal.from_value('cat').crow()
            mewing
        """
        return [x for x in cls.__members__.values() if x.value[0] == value][0]

    def to_value(self, ignore_none, force_value):
        return self.symbol
