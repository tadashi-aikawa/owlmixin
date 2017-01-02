# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import TypeVar, List, Dict, Union, Optional, Sequence, Generic, Callable

from . import dictutil

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass

__version__ = '1.0.0b4'

T = TypeVar('T', bound='OwlMixin')
U = TypeVar('U')


class OwlMixin:
    @classmethod
    def from_dict(cls, d, force_snake_case=True):
        # type: (dict, bool) -> T
        return cls(**dictutil.replace_keys(d, {"self": "_self"}, force_snake_case))

    @classmethod
    def from_optional_dict(cls, d, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[T]
        return d and cls.from_dict(d, force_snake_case)

    @classmethod
    def from_dicts(cls, ds, force_snake_case=True):
        # type: (List[dict], bool) -> TList[T]
        return TList([cls.from_dict(d, force_snake_case) for d in ds])

    @classmethod
    def from_optional_dicts(cls, ds, force_snake_case=True):
        # type: (Optional[List[dict]], bool) -> Optional[TList[T]]
        return ds and cls.from_dicts(ds, force_snake_case)

    @classmethod
    def from_dicts_by_key(cls, ds, force_snake_case=True):
        # type: (Dict[Text, dict], bool) -> TDict[T]
        return TDict({k: cls.from_dict(v, force_snake_case) for k, v in ds.items()})

    @classmethod
    def from_optional_dicts_by_key(cls, ds, force_snake_case=True):
        # type: (Optional[dict], bool) -> Optional[TDict[T]]
        return ds and cls.from_dicts_by_key(ds, force_snake_case)

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
        # type: (Text, Optional[Sequence[Text]], bool) -> TList[T]
        return cls.from_dicts(dictutil.load_csv(csvfile, fieldnames), force_snake_case=force_snake_case)

    @classmethod
    def from_json_url(cls, url, force_snake_case=True):
        # type: (Text, bool) -> T
        return cls.from_dict(dictutil.load_json_url(url), force_snake_case)

    def to_dict(self, ignore_none=False):
        # type: (bool) -> dict
        if isinstance(self, TList):
            raise RuntimeError("TList must not call this method. Please use `to_dicts()` alternatively.")

        return self._traverse_dict(self._to_dict(), ignore_none)

    def to_dicts(self, ignore_none=False):
        # type: (bool) -> List[dict]
        if not isinstance(self, TList):
            raise RuntimeError("Must not call this method except TList. Please use `to_dict()` alternatively.")

        return self._traverse(None, self, ignore_none)

    def to_json(self, indent=None, ignore_none=False):
        # type: (int, bool) -> Text
        func = self.to_dicts if isinstance(self, TList) else self.to_dict
        return dictutil.dump_json(func(ignore_none), indent)

    def to_pretty_json(self, ignore_none=False):
        # type: (bool) -> Text
        return self.to_json(4, ignore_none)

    def to_yaml(self, ignore_none=False):
        # type: (bool) -> Text
        func = self.to_dicts if isinstance(self, TList) else self.to_dict
        return dictutil.dump_yaml(func(ignore_none))

    def _to_dict(self):
        # type: () -> dict
        """
        please override this method and return dict you want,
        if you want to place special handling between conversion from instance variable to dict.
        """
        return self.__dict__

    def _traverse_dict(self, instance_dict, ignore_none):
        return {k: self._traverse(k, v, ignore_none) for k, v in instance_dict.items() if not (ignore_none and v is None)}

    def _traverse_list(self, instance_list, ignore_none):
        return [self._traverse(None, i, ignore_none) for i in instance_list]

    def _traverse(self, key, value, ignore_none=False):
        if isinstance(value, OwlMixin) and not isinstance(value, (TList, TDict)):
            return value.to_dict(ignore_none)
        elif isinstance(value, dict):
            return self._traverse_dict(value, ignore_none)
        elif isinstance(value, list):
            return self._traverse_list(value, ignore_none)
        else:
            return value


class TList(list, Generic[T], OwlMixin):
    def map(self, func):
        # type: (Callable[[T], U]) -> TList[U]
        return TList(map(func, self))

    def filter(self, func):
        # type: (Callable[[T], bool]) -> TList[T]
        return TList(filter(func, self))

    def group_by(self, to_key):
        # type: (Callable[[T], Text]) -> TDict[TList[T]]
        ret = TDict()
        for v in self:
            k = to_key(v)
            ret.setdefault(k, TList())
            ret[k].append(v)
        return ret


class TDict(dict, Generic[T], OwlMixin):
    def map(self, func):
        # type: (Callable[[T], U]) -> TList[U]
        return TList(map(func, [v for k, v in sorted(self.items())]))

    def filter(self, func):
        # type: (Callable[[T], bool]) -> TList[T]
        return TList(filter(func, [v for k, v in sorted(self.items())]))

    def _to_dict(self):
        # type: () -> dict
        return dict(self)
