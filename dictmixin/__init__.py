# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import json
import yaml
from yaml import Loader, SafeLoader

from typing import TypeVar, List, Dict, Union, Optional

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass

__title__ = 'dictmixin'
__version__ = '0.6.0'
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

    def to_dict(self, ignore_none=False):
        # type: (bool) -> dict
        return self._traverse_dict(self.__dict__, ignore_none)

    def to_json(self, indent=None, ignore_none=False):
        # type: (int, bool) -> Text
        return json.dumps(self.to_dict(ignore_none),
                          indent=indent,
                          ensure_ascii=False,
                          sort_keys=True,
                          separators=(',', ': '))

    def to_pretty_json(self, ignore_none=False):
        # type: (bool) -> Text
        return self.to_json(4, ignore_none)

    def to_yaml(self, ignore_none=False):
        # type: (bool) -> Text
        return yaml.dump(self.to_dict(ignore_none),
                         indent=2,
                         encoding=None,
                         allow_unicode=True,
                         default_flow_style=False,
                         Dumper=MyDumper)

    def _traverse_dict(self, instance_dict, ignore_none):
        return {k: self._traverse(k, v, ignore_none) for k, v in instance_dict.items() if not (ignore_none and v is None)}

    def _traverse(self, key, value, ignore_none=False):
        if isinstance(value, DictMixin):
            return value.to_dict(ignore_none)
        elif isinstance(value, dict):
            return self._traverse_dict(value, ignore_none)
        elif isinstance(value, list):
            return [self._traverse(key, i, ignore_none) for i in value]
        elif hasattr(value, '__dict__'):
            return self._traverse_dict(value.__dict__, ignore_none)
        else:
            return value
