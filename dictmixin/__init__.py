# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import re
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
__version__ = '0.7.1'
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


def replace_keys(d, keymap, force_snake_case):
    # type: (dict, Dict[Text, Text], bool) -> Dict[Text, Text]
    return {
        to_snake(keymap.get(k, k)) if force_snake_case else keymap.get(k, k):
            v for k, v in d.items()
        }


def to_snake(value):
    # type: (Text) -> Text
    # For key of dictionary
    return re.sub(r'((?<!^)[A-Z])', "_\\1", value).lower().replace("-", "_")


class DictMixin:
    @classmethod
    def from_dict(cls, d, force_snake_case=True):
        # type: (dict, bool) -> T
        return cls(**replace_keys(d, {"self": "_self"}, force_snake_case))

    @classmethod
    def from_optional_dict(cls, d, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[T]
        return cls.from_dict(d, force_snake_case) if d is not None else None

    @classmethod
    def from_dict2list(cls, ds, force_snake_case=True):
        # type: (List[dict], bool) -> List[T]
        return [cls.from_dict(d, force_snake_case) for d in ds]

    @classmethod
    def from_optional_dict2list(cls, ds, force_snake_case=True):
        # type: (Optional[List[dict]], bool) -> Optional[List[T]]
        return cls.from_dict2list(ds, force_snake_case) if ds is not None else None

    @classmethod
    def from_dict2dict(cls, ds, force_snake_case=True):
        # type: (dict, bool) -> Dict[Text, T]
        return {k: cls.from_dict(v, force_snake_case) for k, v in ds.items()}

    @classmethod
    def from_optional_dict2dict(cls, ds, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[Dict[Text, T]]
        return cls.from_dict2dict(ds, force_snake_case) if ds is not None else None

    @classmethod
    def from_json(cls, data, force_snake_case=True):
        # type: (Text, bool) -> T
        return cls.from_dict(json.loads(data), force_snake_case)

    @classmethod
    def from_yaml(cls, data, force_snake_case=True):
        # type: (Union[Text, file], bool) -> T
        return cls.from_dict(yaml.load(data), force_snake_case)

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
