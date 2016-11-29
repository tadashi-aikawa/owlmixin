# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import json
import yaml
from yaml import Loader, SafeLoader

from typing import TypeVar, List, Dict, Text, Union

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


def construct_yaml_str(self, node):
    return self.construct_scalar(node)


Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


class DictMixin:
    @classmethod
    def from_dict(cls, d):
        # type: (dict) -> T
        return cls(**d)

    @classmethod
    def from_dict2list(cls, ds):
        # type: (List[dict]) -> List[T]
        return [cls(**d) for d in ds]

    @classmethod
    def from_dict2dict(cls, ds):
        # type: (dict) -> Dict[Text, T]
        return {k: cls(**v) for k, v in ds.items()}

    @classmethod
    def from_json(cls, data):
        # type: (Text) -> T
        return cls.from_dict(json.loads(data))

    @classmethod
    def from_yaml(cls, data):
        # type: (Union[Text, file]) -> T
        return cls.from_dict(yaml.load(data))

    def to_dict(self):
        # type: () -> dict
        return self._traverse_dict(self.__dict__)

    def to_json(self, indent=0):
        # type: () -> Text
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False, sort_keys=True)

    def to_pretty_json(self):
        # type: () -> Text
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
