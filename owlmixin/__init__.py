# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import TypeVar, List, Dict, Optional

from owlmixin.owlcollections import TList, TDict
from owlmixin import util
from owlmixin.transformers import DictTransformer, JsonTransformer, YamlTransformer, traverse_dict

__version__ = '1.0.0rc14'

T = TypeVar('T', bound='OwlMixin')


class OwlMixin(DictTransformer, JsonTransformer, YamlTransformer):
    @property
    def _dict(self):
        return self.__dict__

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

            >>> from owlmixin.samples import Human, Food
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

        If you don't set `force_snake=False` explicitly, keys are transformed to snake case as following.

            >>> human = Human.from_dict({
            ...     "--id": 1,
            ...     "<name>": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "namesByLang": {"en": "Apple"}}
            ...     ]
            ... })
            >>> human.id
            1
            >>> human.name
            'Tom'
            >>> human.favorites[0].names_by_lang["en"]
            'Apple'

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

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dict(None)
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

            >>> from owlmixin.samples import Human
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

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts(None)
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

            >>> from owlmixin.samples import Human
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

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts_by_key(None)
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

            >>> from owlmixin.samples import Human
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

            >>> from owlmixin.samples import Human
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

            >>> from owlmixin.samples import Human
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

            >>> from owlmixin.samples import Human
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
