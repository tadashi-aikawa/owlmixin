# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import functools
from typing import TypeVar, List, Dict, Union, Optional, Generic, Callable

from . import util


__version__ = '1.0.0rc8'

T = TypeVar('T')
U = TypeVar('U')
K = TypeVar('K')


class OwlMixin:
    @classmethod
    def from_dict(cls, d, force_snake_case=True):
        """From dict to instance

        :param dict d: Dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls(**util.replace_keys(d, {"self": "_self"}, force_snake_case))

    @classmethod
    def from_optional_dict(cls, d, force_snake_case=True):
        """From dict to instance. If d is None, return None.

        :param Optional[dict] d: Dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: Optional[T]
        """
        return d and cls.from_dict(d, force_snake_case)

    @classmethod
    def from_dicts(cls, ds, force_snake_case=True):
        """From list of dict to list of instance

        :param List[dict] ds: List of dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: TList[T]
        """
        return TList([cls.from_dict(d, force_snake_case) for d in ds])

    @classmethod
    def from_optional_dicts(cls, ds, force_snake_case=True):
        """From list of dict to list of instance. If ds is None, return None.

        :param Optional[List[dict]] ds: List of dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: Optional[TList[T]]
        """
        return ds and cls.from_dicts(ds, force_snake_case)

    @classmethod
    def from_dicts_by_key(cls, ds, force_snake_case=True):
        """From dict of dict to dict of instance

        :param Dict[unicode, dict] ds: Dict of dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Dict of instance
        :rtype: TDict[T]
        """
        return TDict({k: cls.from_dict(v, force_snake_case) for k, v in ds.items()})

    @classmethod
    def from_optional_dicts_by_key(cls, ds, force_snake_case=True):
        """From dict of dict to dict of instance. If ds is None, return None.

        :param Optional[Dict[unicode, dict]] ds: Dict of dict
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Dict of instance
        :rtype: Optional[TDict[T]]
        """
        return ds and cls.from_dicts_by_key(ds, force_snake_case)

    @classmethod
    def from_json(cls, data, force_snake_case=True):
        """From json string to instance

        :param unicode data: Json string
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_json(data), force_snake_case)

    @classmethod
    def from_jsonf(cls, fpath, encoding='utf8', force_snake_case=True):
        """From json file path to instance

        :param unicode fpath: Json file path
        :param unicode encoding: Json file encoding
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_jsonf(fpath, encoding), force_snake_case)

    @classmethod
    def from_json_to_list(cls, data, force_snake_case=True):
        """From json string to list of instance

        :param unicode data: Json string
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_json(data), force_snake_case)

    @classmethod
    def from_jsonf_to_list(cls, fpath, encoding='utf8', force_snake_case=True):
        """From json file path to list of instance

        :param unicode fpath: Json file path
        :param unicode encoding: Json file encoding
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_jsonf(fpath, encoding), force_snake_case)

    @classmethod
    def from_yaml(cls, data, force_snake_case=True):
        """From yaml string to instance

        :param unicode data: Yaml string
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_yaml(data), force_snake_case)

    @classmethod
    def from_yamlf(cls, fpath, encoding='utf8', force_snake_case=True):
        """From yaml file path to instance

        :param unicode fpath: Yaml file path
        :param unicode encoding: Yaml file encoding
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_yamlf(fpath, encoding), force_snake_case)

    @classmethod
    def from_yaml_to_list(cls, data, force_snake_case=True):
        """From yaml string to list of instance

        :param unicode data: Yaml string
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_yaml(data), force_snake_case)

    @classmethod
    def from_yamlf_to_list(cls, fpath, encoding='utf8', force_snake_case=True):
        """From yaml file path to list of instance

        :param unicode fpath: Yaml file path
        :param unicode encoding: Yaml file encoding
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_yamlf(fpath, encoding), force_snake_case)

    @classmethod
    def from_csvf(cls, fpath, fieldnames=None, encoding='utf8', force_snake_case=True):
        """From csv file path to list of instance

        :param unicode fpath: Csv file path
        :param Optional[Sequence[unicode]] fieldnames: Specify csv header names if not included in the file
        :param unicode encoding: Csv file encoding
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of Instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_csvf(fpath, fieldnames, encoding), force_snake_case=force_snake_case)

    @classmethod
    def from_json_url(cls, url, force_snake_case=True):
        """From url which returns json to instance

        :param unicode url: Url which returns json
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_json_url(url), force_snake_case)

    def to_dict(self, ignore_none=True):
        """From instance to dict

        :param bool ignore_none: Properties which is None are excluded if True
        :return: Dict
        :rtype: dict
        """
        if isinstance(self, TList):
            raise RuntimeError("TList must not call this method. Please use `to_dicts()` alternatively.")

        return self._traverse_dict(self._to_dict(), ignore_none)

    def to_dicts(self, ignore_none=True):
        """From instance to list of dict

        :param bool ignore_none: Properties which is None are excluded if True
        :return: List of dict
        :rtype: List[dict]
        """
        if not isinstance(self, TList):
            raise RuntimeError("Must not call this method except TList. Please use `to_dict()` alternatively.")

        return self._traverse(self, ignore_none)

    def to_json(self, indent=None, ignore_none=True):
        """From instance to json string

        :param Optional[int] indent: Number of indentation
        :param bool ignore_none: Properties which is None are excluded if True
        :return: Json string
        :rtype: unicode
        """
        func = self.to_dicts if isinstance(self, TList) else self.to_dict
        return util.dump_json(func(ignore_none), indent)

    def to_pretty_json(self, ignore_none=True):
        """From instance to pretty json string

        :param bool ignore_none: Properties which is None are excluded if True
        :return: Json string
        :rtype: unicode
        """
        return self.to_json(4, ignore_none)

    def to_yaml(self, ignore_none=True):
        """From instance to yaml string

        :param bool ignore_none: Properties which is None are excluded if True
        :return: Yaml string
        :rtype: unicode
        """
        func = self.to_dicts if isinstance(self, TList) else self.to_dict
        return util.dump_yaml(func(ignore_none))

    def _to_dict(self):
        """please override this method and return dict you want,
        if you want to place special handling between conversion from instance variable to dict.

        :return: Dict
        :rtype: dict
        """
        return self.__dict__

    def _traverse_dict(self, instance_dict, ignore_none):
        return {k: self._traverse(v, ignore_none) for
                k, v in instance_dict.items()
                if not (ignore_none and v is None)}

    def _traverse_list(self, instance_list, ignore_none):
        return [self._traverse(i, ignore_none) for i in instance_list]

    def _traverse(self, value, ignore_none=True):
        if isinstance(value, OwlMixin) and not isinstance(value, (TList, TDict)):
            return value.to_dict(ignore_none)
        elif isinstance(value, dict):
            return self._traverse_dict(value, ignore_none)
        elif isinstance(value, list):
            return self._traverse_list(value, ignore_none)
        else:
            return value


class TList(list, Generic[T], OwlMixin):
    def __add__(self, values):
        # type: (TList[T]) -> TList[T]
        return TList(values + list(self))

    def to_csv(self, fieldnames, with_header=False, crlf=False):
        """From sequence of text to csv string

        :param Sequence[unicode] fieldnames: Order of columns by property name
        :param bool with_header: Add headers at the first line if True
        :param bool crlf: Add CRLF line break at the end of line if True, else add LF
        :return: Csv string
        :rtype: unicode
        """
        # type: (Sequence[Text], bool, bool) -> Text
        return util.dump_csv(self.to_dicts(), fieldnames, with_header, crlf)

    def map(self, func):
        """
        :param (T) -> U func:
        :rtype: TList[U]
        """
        return TList(map(func, self))

    def filter(self, func):
        """
        :param (T) -> bool func:
        :rtype: TList[T]
        """
        return TList([x for x in self if func(x)])

    def reject(self, func):
        """
        :param (T) -> bool func:
        :rtype: TList[T]
        """
        return TList([x for x in self if not func(x)])

    def group_by(self, to_key):
        """
        :param (T) -> unicode to_key:
        :rtype: TDict[TList[T]]
        """
        ret = TDict()
        for v in self:
            k = to_key(v)
            ret.setdefault(k, TList())
            ret[k].append(v)
        return ret

    def order_by(self, func, reverse=False):
        """
        :param (T) -> any func:
        :param bool reverse: Sort by descend order if True, else by ascend
        :rtype: TDict[TList[T]]
        """
        return TList(sorted(self, key=func, reverse=reverse))

    def concat(self, values):
        """
        :param TList[T] values:
        :rtype: TList[T]
        """
        return self + values

    def reduce(self, func, init_value):
        """
        :param (U, T) -> U func:
        :param U init_value:
        :rtype: U
        """
        return functools.reduce(func, self, init_value)

    def sum(self):
        """
        :rtype: int | float
        """
        return sum(self)

    def sum_by(self, func):
        """
        :param (T) -> int | float func:
        :rtype: int | float
        """
        # type: (Callable[[T], Union[int, float]]) -> Union[int, float]
        return self.map(func).sum()

    def size(self):
        """
        :rtype: int
        """
        return len(self)

    def join(self, joint):
        """
        :param unicode joint:
        :rtype: unicode
        """
        return joint.join(self)

    def find(self, func):
        """
        :param (T) -> bool func:
        :rtype: T
        """
        for x in self:
            if func(x):
                return x

    def all(self, func):
        """
        :param (T) -> bool func:
        :rtype: T
        """
        return all([func(x) for x in self])

    def any(self, func):
        """
        :param (T) -> bool func:
        :rtype: T
        """
        return any([func(x) for x in self])


class TDict(dict, Generic[T], OwlMixin):
    def map(self, func):
        """
        :param (K, T) -> U func:
        :rtype: TList[U]
        """
        return TList([func(k, v) for k, v in self.items()])

    def map_values(self, func):
        """
        :param (T) -> U func:
        :rtype: TDict[U]
        """
        return TDict({k: func(v) for k, v in self.items()})

    def filter(self, func):
        """
        :param (K, T) -> bool func:
        :rtype: TList[T]
        """
        return TList([v for k, v in self.items() if func(k, v)])

    def reject(self, func):
        """
        :param (K, T) -> bool func:
        :rtype: TList[T]
        """
        return TList([v for k, v in self.items() if not func(k, v)])

    def sum(self):
        """
        :rtype: int | float
        """
        return sum(self.values())

    def sum_by(self, func):
        """
        :param (K, T) -> int | float func:
        :rtype: int | float
        """
        return self.map(func).sum()

    def size(self):
        """
        :rtype: int
        """
        return len(self)

    def find(self, func):
        """
        :param (K, T) -> bool func:
        :rtype: T
        """
        for k, v in self.items():
            if func(k, v):
                return v

    def to_values(self):
        """
        :rtype: TList[T]
        """
        return TList(self.values())

    def _to_dict(self):
        return dict(self)

    def all(self, func):
        """
        :param (K, T) -> bool func:
        :rtype: T
        """
        return all([func(k, v) for k, v in self.items()])

    def any(self, func):
        """
        :param (K, T) -> bool func:
        :rtype: T
        """
        return any([func(k, v) for k, v in self.items()])
