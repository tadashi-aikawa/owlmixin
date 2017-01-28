# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import functools
from typing import TypeVar, List, Dict, Union, Optional, Generic, Callable

from . import util


__version__ = '1.0.0rc9'

T = TypeVar('T', bound='OwlMixin')
U = TypeVar('U')
K = TypeVar('K')


class OwlMixin:
    @classmethod
    def from_dict(cls, d, force_snake_case=True):
        """From dict to instance

        :param d: Dict
        :type d: dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T

        Usage:

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            >>> human.id
            1
            >>> human.name
            'Tom'
            >>> human.favorites[0].name
            'Apple'
            >>> human.favorites[0].names_by_lang["de"]
            'Apfel'

        Automatic camel case conversion:

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "namesByLang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            >>> human.favorites[0].names_by_lang["de"]
            'Apfel'

        You can allow extra parameters (like ``hogehoge``) if the class has ``**extra`` argument.

            >>> apple = Food.from_dict({
            ...     "name": "Apple",
            ...     "hogehoge": "ooooooooooooooooooooo",
            ... })
            >>> apple.to_dict()
            {'name': 'Apple'}

        You can prohibit extra parameters (like ``hogehoge``) if the class does not have ``**extra`` argument.

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "hogehoge": "ooooooooooooooooooooo",
            ...     "favorites": [
            ...         {"name": "Apple", "namesByLang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            Traceback (most recent call last):
                ...
            TypeError: __init__() got an unexpected keyword argument 'hogehoge'

        """
        return cls(**util.replace_keys(d, {"self": "_self"}, force_snake_case))

    @classmethod
    def from_optional_dict(cls, d, force_snake_case=True):
        """From dict to instance. If d is None, return None.

        :param d: Dict
        :type d: Optional[dict]
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: Optional[T]

        Usage:

            >>> Human.from_optional_dict(None)
            >>> None
        """
        return d and cls.from_dict(d, force_snake_case)

    @classmethod
    def from_dicts(cls, ds, force_snake_case=True):
        """From list of dict to list of instance

        :param ds: List of dict
        :type ds: List[dict]
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of instance
        :rtype: TList[T]

        Usage:

            >>> humans = Human.from_dicts([
            ...    {"id": 1, "name": "Tom", "favorites": [{"name": "Apple"}]},
            ...    {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ])
            >>> humans[0].name
            'Tom'
            >>> humans[1].name
            'John'
        """
        return TList([cls.from_dict(d, force_snake_case) for d in ds])

    @classmethod
    def from_optional_dicts(cls, ds, force_snake_case=True):
        """From list of dict to list of instance. If ds is None, return None.

        :param ds: List of dict
        :type ds: Optional[List[dict]]
        :param bool force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of instance
        :rtype: Optional[TList[T]]

        Usage:

            >>> Human.from_optional_dicts(None)
            >>> None
        """
        return ds and cls.from_dicts(ds, force_snake_case)

    @classmethod
    def from_dicts_by_key(cls, ds, force_snake_case=True):
        """From dict of dict to dict of instance

        :param ds: Dict of dict
        :type ds: Dict[unicode, dict]
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Dict of instance
        :rtype: TDict[T]

        Usage:

            >>> humans_by_name = Human.from_dicts_by_key({
            ...    'Tom':  {"id": 1, "name": "Tom",  "favorites": [{"name": "Apple"}]},
            ...    'John': {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... })
            >>> humans_by_name['Tom'].name
            'Tom'
            >>> humans_by_name['John'].name
            'John'
        """
        return TDict({k: cls.from_dict(v, force_snake_case) for k, v in ds.items()})

    @classmethod
    def from_optional_dicts_by_key(cls, ds, force_snake_case=True):
        """From dict of dict to dict of instance. If ds is None, return None.

        :param ds: Dict of dict
        :type ds: Optional[Dict[unicode, dict]]
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Dict of instance
        :rtype: Optional[TDict[T]]

        Usage:

            >>> Human.from_optional_dicts_by_key(None)
            >>> None
        """
        return ds and cls.from_dicts_by_key(ds, force_snake_case)

    @classmethod
    def from_json(cls, data, force_snake_case=True):
        """From json string to instance

        :param data: Json string
        :type data: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T

        Usage:

            >>> human = Human.from_json('''{
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... }''')
            >>> human.id
            1
            >>> human.name
            'Tom'
            >>> human.favorites[0].names_by_lang["de"]
            'Apfel'
        """
        return cls.from_dict(util.load_json(data), force_snake_case)

    @classmethod
    def from_jsonf(cls, fpath, encoding='utf8', force_snake_case=True):
        """From json file path to instance

        :param fpath: Json file path
        :type fpath: unicode
        :param encoding: Json file encoding
        :type encoding: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_jsonf(fpath, encoding), force_snake_case)

    @classmethod
    def from_json_to_list(cls, data, force_snake_case=True):
        """From json string to list of instance

        :param data: Json string
        :type data: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of instance
        :rtype: TList[T]

        Usage:

            >>> humans = Human.from_json_to_list('''[
            ...    {"id": 1, "name": "Tom",  "favorites": [{"name": "Apple"}]},
            ...    {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ]''')
            >>> humans[0].name
            'Tom'
            >>> humans[1].name
            'John'
        """
        return cls.from_dicts(util.load_json(data), force_snake_case)

    @classmethod
    def from_jsonf_to_list(cls, fpath, encoding='utf8', force_snake_case=True):
        """From json file path to list of instance

        :param fpath: Json file path
        :type fpath: unicode
        :param encoding: Json file encoding
        :type encoding: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_jsonf(fpath, encoding), force_snake_case)

    @classmethod
    def from_yaml(cls, data, force_snake_case=True):
        """From yaml string to instance

        :param data: Yaml string
        :type data: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T

        Usage:

            >>> human = Human.from_yaml('''
            ... id: 1
            ... name: Tom
            ... favorites:
            ...   - name: Apple
            ...     names_by_lang:
            ...       en: Apple
            ...       de: Apfel
            ...   - name: Orange
            ... ''')
            >>> human.id
            1
            >>> human.name
            'Tom'
            >>> human.favorites[0].names_by_lang["de"]
            'Apfel'
        """
        return cls.from_dict(util.load_yaml(data), force_snake_case)

    @classmethod
    def from_yamlf(cls, fpath, encoding='utf8', force_snake_case=True):
        """From yaml file path to instance

        :param fpath: Yaml file path
        :type fpath: unicode
        :param encoding: Yaml file encoding
        :type encoding: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_yamlf(fpath, encoding), force_snake_case)

    @classmethod
    def from_yaml_to_list(cls, data, force_snake_case=True):
        """From yaml string to list of instance

        :param data: Yaml string
        :type data: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of instance
        :rtype: TList[T]

        Usage:

            >>> humans = Human.from_yaml_to_list('''
            ... - id: 1
            ...   name: Tom
            ...   favorites:
            ...     - name: Apple
            ... - id: 2
            ...   name: John
            ...   favorites:
            ...     - name: Orange
            ... ''')
            >>> humans[0].name
            'Tom'
            >>> humans[1].name
            'John'
            >>> humans[0].favorites[0].name
            'Apple'
        """
        return cls.from_dicts(util.load_yaml(data), force_snake_case)

    @classmethod
    def from_yamlf_to_list(cls, fpath, encoding='utf8', force_snake_case=True):
        """From yaml file path to list of instance

        :param fpath: Yaml file path
        :type fpath: unicode
        :param encoding: Yaml file encoding
        :type encoding: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_yamlf(fpath, encoding), force_snake_case)

    @classmethod
    def from_csvf(cls, fpath, fieldnames=None, encoding='utf8', force_snake_case=True):
        """From csv file path to list of instance

        :param fpath: Csv file path
        :type fpath: unicode
        :param fieldnames: Specify csv header names if not included in the file
        :type fieldnames: Optional[Sequence[unicode]]
        :param encoding: Csv file encoding
        :type encoding: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: List of Instance
        :rtype: TList[T]
        """
        return cls.from_dicts(util.load_csvf(fpath, fieldnames, encoding), force_snake_case=force_snake_case)

    @classmethod
    def from_json_url(cls, url, force_snake_case=True):
        """From url which returns json to instance

        :param url: Url which returns json
        :type url: unicode
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :type force_snake_case: bool
        :return: Instance
        :rtype: T
        """
        return cls.from_dict(util.load_json_url(url), force_snake_case)

    def to_dict(self, ignore_none=True):
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Dict
        :rtype: dict

        Usage:

            >>> human_dict = {
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...     ]
            ... }
            >>> Human.from_dict(human_dict).to_dict() == human_dict
            True

        You can include None properties by specifying None for ignore_none

            >>> f = Food.from_dict({"name": "Apple"}).to_dict(ignore_none=False)
            >>> f["name"]
            'Apple'
            >>> "names_by_lang" in f
            True
            >>> f["names_by_lang"]

        As default

            >>> f = Food.from_dict({"name": "Apple"}).to_dict()
            >>> f["name"]
            'Apple'
            >>> "names_by_lang" in f
            False

        """
        if isinstance(self, TList):
            raise RuntimeError("TList must not call this method. Please use `to_dicts()` alternatively.")

        return self._traverse_dict(self._to_dict(), ignore_none)

    def to_dicts(self, ignore_none=True):
        """From instance to list of dict

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: List of dict
        :rtype: List[dict]

        Usage:

            >>> human_dicts = [
            ...     {"id": 1, "name": "Tom", "favorites": [{"name": "Apple"}]},
            ...     {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ]
            >>> Human.from_dicts(human_dicts).to_dicts() == human_dicts
            True
        """
        if not isinstance(self, TList):
            raise RuntimeError("Must not call this method except TList. Please use `to_dict()` alternatively.")

        return self._traverse(self, ignore_none)

    def to_json(self, indent=None, ignore_none=True):
        """From instance to json string

        :param indent: Number of indentation
        :type indent: Optional[int]
        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Json string
        :rtype: unicode

        Usage:

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            >>> human.to_json()
            '{"favorites": [{"name": "Apple","names_by_lang": {"de": "Apfel","en": "Apple"}},{"name": "Orange"}],"id": 1,"name": "Tom"}'
        """
        func = self.to_dicts if isinstance(self, TList) else self.to_dict
        return util.dump_json(func(ignore_none), indent)

    def to_pretty_json(self, ignore_none=True):
        """From instance to pretty json string

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Json string
        :rtype: unicode

        Usage:

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            >>> print(human.to_pretty_json())
            {
                "favorites": [
                    {
                        "name": "Apple",
                        "names_by_lang": {
                            "de": "Apfel",
                            "en": "Apple"
                        }
                    },
                    {
                        "name": "Orange"
                    }
                ],
                "id": 1,
                "name": "Tom"
            }
        """
        return self.to_json(4, ignore_none)

    def to_yaml(self, ignore_none=True):
        """From instance to yaml string

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Yaml string
        :rtype: unicode

        Usage:

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })
            >>> print(human.to_yaml())
            favorites:
              - name: Apple
                names_by_lang:
                  de: Apfel
                  en: Apple
              - name: Orange
            id: 1
            name: Tom
            <BLANKLINE>
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

        :param fieldnames: Order of columns by property name
        :type fieldnames: Sequence[unicode]
        :param with_header: Add headers at the first line if True
        :type with_header: bool
        :param crlf: Add CRLF line break at the end of line if True, else add LF
        :type crlf: bool
        :return: Csv string
        :rtype: unicode

        Usage:

            >>> humans = Human.from_dicts([
            ...     {"id": 1, "name": "Tom", "favorites": [{"name": "Apple"}]},
            ...     {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ])
            >>> print(humans.to_csv(fieldnames=['name', 'id', 'favorites']))
            Tom,1,[{'name': 'Apple'}]
            John,2,[{'name': 'Orange'}]
            <BLANKLINE>
            >>> print(humans.to_csv(fieldnames=['name', 'id', 'favorites'], with_header=True))
            name,id,favorites
            Tom,1,[{'name': 'Apple'}]
            John,2,[{'name': 'Orange'}]
            <BLANKLINE>
        """
        return util.dump_csv(self.to_dicts(), fieldnames, with_header, crlf)

    def map(self, func):
        """
        :param func:
        :type func: T -> U
        :rtype: TList[U]

        Usage:

            >>> TList([1, 2, 3, 4, 5]).map(lambda x: x+1)
            [2, 3, 4, 5, 6]
        """
        return TList(map(func, self))

    def filter(self, func):
        """
        :param func:
        :type func: T -> bool
        :rtype: TList[T]

        Usage:

            >>> TList([1, 2, 3, 4, 5]).filter(lambda x: x > 3)
            [4, 5]
        """
        return TList([x for x in self if func(x)])

    def reject(self, func):
        """
        :param func:
        :type func: T -> bool
        :rtype: TList[T]

        Usage:

            >>> TList([1, 2, 3, 4, 5]).reject(lambda x: x > 3)
            [1, 2, 3]
        """
        return TList([x for x in self if not func(x)])

    def group_by(self, to_key):
        """
        :param to_key:
        :type to_key: T -> unicode
        :rtype: TDict[TList[T]]

        Usage:

            >>> TList([1, 2, 3, 4, 5]).group_by(lambda x: x % 2).to_json()
            '{"0": [2,4],"1": [1,3,5]}'
        """
        ret = TDict()
        for v in self:
            k = to_key(v)
            ret.setdefault(k, TList())
            ret[k].append(v)
        return ret

    def order_by(self, func, reverse=False):
        """
        :param func:
        :type func: T -> any
        :param reverse: Sort by descend order if True, else by ascend
        :type reverse: bool
        :rtype: TList[T]

        Usage:

            >>> TList([12, 25, 31, 40, 57]).order_by(lambda x: x % 10)
            [40, 31, 12, 25, 57]
            >>> TList([12, 25, 31, 40, 57]).order_by(lambda x: x % 10, reverse=True)
            [57, 25, 12, 31, 40]
        """
        return TList(sorted(self, key=func, reverse=reverse))

    def concat(self, values):
        """
        :param values:
        :type values: TList[T]
        :rtype: TList[T]

        Usage:

            >>> TList([1, 2]).concat(TList([3, 4]))
            [1, 2, 3, 4]
        """
        return self + values

    def reduce(self, func, init_value):
        """
        :param func:
        :type func: (U, T) -> U
        :param init_value:
        :type init_value: U
        :rtype: U

        Usage:

            >>> TList([1, 2, 3, 4, 5]).reduce(lambda t, x: t + 2*x, 100)
            130
        """
        return functools.reduce(func, self, init_value)

    def sum(self):
        """
        :rtype: int | float

        Usage:

            >>> TList([1, 2, 3, 4, 5]).sum()
            15
        """
        return sum(self)

    def sum_by(self, func):
        """
        :param func:
        :type func: T -> int | float
        :rtype: int | float

        Usage:

            >>> TList([1, 2, 3, 4, 5]).sum_by(lambda x: x*2)
            30
        """
        return self.map(func).sum()

    def size(self):
        """
        :rtype: int

        Usage:

            >>> TList([1, 2, 3, 4, 5]).size()
            5
        """
        return len(self)

    def join(self, joint):
        """
        :param joint:
        :type joint: unicode
        :rtype: unicode

        Usage:

            >>> TList(['A', 'B', 'C']).join("-")
            'A-B-C'
        """
        return joint.join(self)

    def find(self, func):
        """
        :param func:
        :type func: T -> bool
        :rtype: T

        Usage:

            >>> TList([1, 2, 3, 4, 5]).find(lambda x: x > 3)
            4
        """
        for x in self:
            if func(x):
                return x

    def all(self, func):
        """
        :param func:
        :type func: T -> bool
        :rtype: T

        Usage:

            >>> TList([1, 2, 3, 4, 5]).all(lambda x: x > 0)
            True
            >>> TList([1, 2, 3, 4, 5]).all(lambda x: x > 1)
            False
        """
        return all([func(x) for x in self])

    def any(self, func):
        """
        :param func:
        :type func: T -> bool
        :rtype: T

        Usage:

            >>> TList([1, 2, 3, 4, 5]).any(lambda x: x > 4)
            True
            >>> TList([1, 2, 3, 4, 5]).any(lambda x: x > 5)
            False
        """
        return any([func(x) for x in self])


class TDict(dict, Generic[T], OwlMixin):
    def _to_dict(self):
        return dict(self)

    def map(self, func):
        """
        :param func:
        :type func: (K, T) -> U
        :rtype: TList[U]

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> sorted(TDict(machines_by_no).map(lambda k, v: v.name))
            ['777', 'Atom', 'Doraemon']
        """
        return TList([func(k, v) for k, v in self.items()])

    def map_values(self, func):
        """
        :param func:
        :type func: T -> U
        :rtype: TDict[U]

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).map_values(lambda x: x.name) == {
            ...     "no1": "Atom",
            ...     "no2": "Doraemon",
            ...     "no3": "777"
            ... }
            True
        """
        return TDict({k: func(v) for k, v in self.items()})

    def filter(self, func):
        """
        :param func:
        :type func: (K, T) -> bool
        :rtype: TList[T]

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).filter(lambda k, v: v.id < 3).order_by(lambda v: v.id).to_json()
            '[{"id": 1,"name": "Atom"},{"id": 2,"name": "Doraemon"}]'
        """
        return TList([v for k, v in self.items() if func(k, v)])

    def reject(self, func):
        """
        :param func:
        :type func: (K, T) -> bool
        :rtype: TList[T]

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).reject(lambda k, v: v.id < 3).to_json()
            '[{"id": 3,"name": "777"}]'
        """
        return TList([v for k, v in self.items() if not func(k, v)])

    def sum(self):
        """
        :rtype: int | float

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).map_values(lambda x: x.id).sum()
            6
        """
        return sum(self.values())

    def sum_by(self, func):
        """
        :param func:
        :type func: (K, T) -> (int | float)
        :rtype: int | float

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).sum_by(lambda k, v: v.id)
            6
        """
        return self.map(func).sum()

    def size(self):
        """
        :rtype: int

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).size()
            3
        """
        return len(self)

    def find(self, func):
        """
        :param func:
        :type func: (K, T) -> bool
        :rtype: T

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).find(lambda k, v: v.id == 2).to_json()
            '{"id": 2,"name": "Doraemon"}'
        """
        for k, v in self.items():
            if func(k, v):
                return v

    def to_values(self):
        """
        :rtype: TList[T]

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).to_values().order_by(lambda x: x.id).to_json()
            '[{"id": 1,"name": "Atom"},{"id": 2,"name": "Doraemon"},{"id": 3,"name": "777"}]'
        """
        return TList(self.values())

    def all(self, func):
        """
        :param func:
        :type func: (K, T) -> bool
        :rtype: bool

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).all(lambda k, v: v.id > 0)
            True
            >>> TDict(machines_by_no).all(lambda k, v: v.id > 1)
            False
        """
        return all([func(k, v) for k, v in self.items()])

    def any(self, func):
        """
        :param func:
        :type func: (K, T) -> bool
        :rtype: bool

        Usage:

            >>> machines_by_no = Machine.from_dicts_by_key({
            ...     "no1": {"id": 1, "name": "Atom"},
            ...     "no2": {"id": 2, "name": "Doraemon"},
            ...     "no3": {"id": 3, "name": "777"}
            ... })
            >>> TDict(machines_by_no).any(lambda k, v: v.id > 2)
            True
            >>> TDict(machines_by_no).any(lambda k, v: v.id > 3)
            False
        """
        return any([func(k, v) for k, v in self.items()])
