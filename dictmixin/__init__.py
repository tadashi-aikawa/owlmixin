# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import TypeVar, List, Dict, Union, Optional

from . import dictutil

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass

__title__ = 'dictmixin'
__version__ = '0.8.0'
__author__ = 'tadashi-aikawa'
__license__ = 'MIT'

T = TypeVar('T', bound='DictMixin')


class DictMixin:
    @classmethod
    def from_dict(cls, d, force_snake_case=True):
        # type: (dict, bool) -> T
        return cls(**dictutil.replace_keys(d, {"self": "_self"}, force_snake_case))

    @classmethod
    def from_optional_dict(cls, d, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[T]
        return cls.from_dict(d, force_snake_case) if d is not None else None

    @classmethod
    def from_dicts(cls, ds, force_snake_case=True):
        # type: (List[dict], bool) -> List[T]
        return [cls.from_dict(d, force_snake_case) for d in ds]

    @classmethod
    def from_optional_dicts(cls, ds, force_snake_case=True):
        # type: (Optional[List[dict]], bool) -> Optional[List[T]]
        return cls.from_dicts(ds, force_snake_case) if ds is not None else None

    @classmethod
    def from_dicts_by_key(cls, ds, force_snake_case=True):
        # type: (dict, bool) -> Dict[Text, T]
        return {k: cls.from_dict(v, force_snake_case) for k, v in ds.items()}

    @classmethod
    def from_optional_dicts_by_key(cls, ds, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[Dict[Text, T]]
        return cls.from_dicts_by_key(ds, force_snake_case) if ds is not None else None

    @classmethod
    def from_json(cls, data, force_snake_case=True):
        # type: (Text, bool) -> T
        return cls.from_dict(dictutil.load_json(data), force_snake_case)

    @classmethod
    def from_yaml(cls, data, force_snake_case=True):
        # type: (Union[Text, file], bool) -> T
        return cls.from_dict(dictutil.load_yaml(data), force_snake_case)

    @classmethod
    def from_csv(cls, csvfile, fieldnames=None, force_snake_case=True):
        # type: (Text, Optional[List[Text]], bool) -> List[T]
        return cls.from_dicts(dictutil.load_csv(csvfile, fieldnames), force_snake_case=force_snake_case)

    def to_dict(self, ignore_none=False):
        # type: (bool) -> dict
        return self._traverse_dict(self.__dict__, ignore_none)

    def to_json(self, indent=None, ignore_none=False):
        # type: (int, bool) -> Text
        return dictutil.dump_json(self.to_dict(ignore_none), indent)

    def to_pretty_json(self, ignore_none=False):
        # type: (bool) -> Text
        return self.to_json(4, ignore_none)

    def to_yaml(self, ignore_none=False):
        # type: (bool) -> Text
        return dictutil.dump_yaml(self.to_dict(ignore_none))

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
