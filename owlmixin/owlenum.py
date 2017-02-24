# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from enum import Enum

from owlmixin.transformers import ValueTransformer


class OwlEnum(ValueTransformer, Enum):
    """ This class is similar to Enum except that can dump as json or yaml
    """
    def to_value(self):
        return self.value
