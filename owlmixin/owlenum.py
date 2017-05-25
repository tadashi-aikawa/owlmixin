# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from enum import Enum
from typing import TypeVar

from owlmixin.transformers import ValueTransformer


T = TypeVar('T', bound='OwlObjectEnum')


class OwlEnum(ValueTransformer, Enum):
    """ This class is similar to Enum except that can dump as json or yaml
    """
    def to_value(self, ignore_none, force_value):
        return self.value


class OwlObjectEnum(ValueTransformer, Enum):
    """ This class is similar to OwlEnum except that can have additional object.
    TODO: Not exec doctest
    """
    def __init__(self, symbol, obj):
        self.symbol = symbol
        self.object = obj

    @classmethod
    def from_symbol(cls, symbol):
        """Create instance from symbol

        :param symbol: unique symbol
        :type symbol: unicode
        :return: This instance
        :rtype: T

        Usage:

            >>> from owlmixin.samples import Animal
            >>> Animal.from_symbol('cat').crow()
            mewing
        """
        return [x for x in cls.__members__.values() if x.value[0] == symbol][0]

    def to_value(self, ignore_none, force_value):
        return self.symbol
