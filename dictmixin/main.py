# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import json

from typing import TypeVar, List

"""
For example::

    class Human(DictMixin):
        def __init__(self, id, name, favorite):
            self.id = id
            self.name = name
            self.favorite = Food.from_dicts(favorite)


    class Food(DictMixin):
        def __init__(self, id, name, color=None):
            self.id = id
            self.name = name
            if color is not None:
                self.color = color

    j = '''
    {
        "id": 10,
        "name": "tadashi",
        "favorite": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "orange", "color": "white"}
        ]
    }
    '''

    d = {
        "id": 10,
        "name": "tadashi",
        "favorite": [
            {"id": 1, "name": "apple"},
            {"id": 2, "name": "orange", "color": "white"}
        ]
    }

    >>> y1 = Human.from_json(j)
    >>> y2 = Human.from_dict(d)
    >>> y1.to_json() == y2.to_json()
    True
"""

T = TypeVar('T', bound='DictMixin')


class DictMixin:
    @classmethod
    def from_dict(cls, d):
        # type: (dict) -> T
        return cls(**d)

    @classmethod
    def from_dicts(cls, ds):
        # type: (List[dict]) -> List[T]
        return [cls(**d) for d in ds]

    @classmethod
    def from_json(cls, data):
        # type: (str) -> T
        return cls.from_dict(json.loads(data))

    def to_dict(self):
        # type: () -> dict
        return self._traverse_dict(self.__dict__)

    def to_json(self, indent=0):
        # type: () -> str
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False, sort_keys=True)

    def to_pretty_json(self):
        # type: () -> str
        return self.to_json(4)

    def _traverse_dict(self, instance_dict):
        output = {}
        for key, value in instance_dict.items():
            output[key] = self._traverse(key, value)
        return output

    def _traverse(self, key, value):
        if isinstance(value, DictMixin):
            return value.to_dict()
        elif isinstance(value, dict):
            return self._traverse_dict(value)
        elif isinstance(value, list):
            return [self._traverse(key, i) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__)
        else:
            return value
