# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import json
import yaml
from yaml import Loader, SafeLoader

from typing import TypeVar, List, Dict, Text, Union, Optional

__title__ = 'dictmixin'
__version__ = '0.5.0'
__author__ = 'tadashi-aikawa'
__license__ = 'MIT'

T = TypeVar('T', bound='DictMixin')


class MyDumper(yaml.SafeDumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(MyDumper, self).increase_indent(flow, False)


def construct_yaml_str(self, node):
    return self.construct_scalar(node)


Loader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)
SafeLoader.add_constructor(u'tag:yaml.org,2002:str', construct_yaml_str)


def replace_keys(d, keymap):
    # type: dict -> Dict[Text, Text]
    return {keymap.get(k, k): v for k, v in d.items()}


class DictMixin:
    @classmethod
    def from_dict(cls, d):
        # type: (dict) -> T
        return cls(**replace_keys(d, {"self": "_self"}))

    @classmethod
    def from_optional_dict(cls, d):
        # type: (Optional[dict]) -> Optional[T]
        return cls.from_dict(d) if d is not None else None

    @classmethod
    def from_dict2list(cls, ds):
        # type: (List[dict]) -> List[T]
        return [cls.from_dict(d) for d in ds]

    @classmethod
    def from_optional_dict2list(cls, ds):
        # type: (Optional[List[dict]]) -> Optional[List[T]]
        return cls.from_dict2list(ds) if ds is not None else None

    @classmethod
    def from_dict2dict(cls, ds):
        # type: (dict) -> Dict[Text, T]
        return {k: cls.from_dict(v) for k, v in ds.items()}

    @classmethod
    def from_optional_dict2dict(cls, ds):
        # type: (Optional[dict]) -> Optional[Dict[Text, T]]
        return cls.from_dict2dict(ds) if ds is not None else None

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
        return json.dumps(self.to_dict(),
                          indent=indent,
                          ensure_ascii=False,
                          sort_keys=True,
                          separators=(',', ': '))

    def to_pretty_json(self):
        # type: () -> Text
        return self.to_json(4)

    def to_yaml(self):
        # type: () -> Text
        return yaml.dump(self.to_dict(),
                         indent=2,
                         encoding=None,
                         allow_unicode=True,
                         default_flow_style=False,
                         Dumper=MyDumper)

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
