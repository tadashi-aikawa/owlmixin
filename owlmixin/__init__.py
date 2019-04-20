# coding: utf-8

from typing import TypeVar, List, Dict, Optional, Tuple, Sequence, Type
import inspect

import owlmixin.version
from owlmixin.errors import RequiredError, UnknownPropertiesError, InvalidTypeError
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum, OwlObjectEnum
from owlmixin import util
from owlmixin.transformers import DictTransformer, JsonTransformer, YamlTransformer, ValueTransformer, traverse_dict, TOption

T = TypeVar('T', bound='OwlMixin')

__version__ = owlmixin.version.__version__


def _is_generic(type):
    return hasattr(type, '__origin__')


def assert_extra(cls_properties, arg_dict, cls):
    extra_keys: set = set(arg_dict.keys()) - set([n for n, t in cls_properties])
    if extra_keys:
        raise UnknownPropertiesError(cls, sorted(extra_keys))


def assert_none(value, type_, cls, name):
    if value is None:
        raise RequiredError(cls, name, type_)


def assert_types(value, types: tuple, cls, name):
    if not isinstance(value, types):
        raise InvalidTypeError(cls, name, value, types, type(value))


def traverse(type_, name, value, cls, force_snake_case: bool, force_cast: bool, restrict: bool):
    if hasattr(type_, '__forward_arg__'):
        # XXX: Only if `_ForwardRef` includes myself
        type_ = cls

    if not _is_generic(type_):
        assert_none(value, type_, cls, name)
        if type_ is any:
            return value
        elif issubclass(type_, OwlMixin):
            assert_types(value, (type_, dict), cls, name)
            return type_.from_dict(value, force_snake_case, force_cast, restrict)
        elif issubclass(type_, ValueTransformer):
            return type_.from_value(value)
        else:
            if force_cast:
                return type_(value)
            else:
                assert_types(value, (type_,), cls, name)
                return value

    o_type = type_.__origin__
    g_type = type_.__args__

    if o_type == TList:
        assert_none(value, type_, cls, name)
        assert_types(value, (list,), cls, name)
        return TList([traverse(g_type[0], f'{name}.{i}', v, cls, force_snake_case, force_cast, restrict)
                      for i, v in enumerate(value)])
    elif o_type == TDict:
        assert_none(value, type_, cls, name)
        assert_types(value, (dict,), cls, name)
        return TDict({k: traverse(g_type[0], f'{name}.{k}', v, cls, force_snake_case, force_cast, restrict)
                      for k, v in value.items()})
    elif o_type == TOption:
        v = value.get() if type(value) == TOption else value
        # TODO: Fot `from_csvf`... need to more simple!!
        if (type(v) == str and v) or (type(v) != str and v is not None):
            return TOption(traverse(g_type[0], name, v, cls, force_snake_case, force_cast, restrict))
        return TOption(None)

    else:
        assert False, f"This generics is not supported {o_type}"


class OwlMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        cls._methods_dict = dict(inspect.getmembers(cls, inspect.ismethod))
        return cls


class OwlMixin(DictTransformer, JsonTransformer, YamlTransformer, metaclass=OwlMeta):

    @classmethod
    def from_dict(cls, d: dict, force_snake_case: bool=True, force_cast: bool=False, restrict: bool=True) -> T:
        """From dict to instance

        :param d: Dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human, Food, Japanese
            >>> human: Human = Human.from_dict({
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
            >>> human.favorites[0].names_by_lang.get()["de"]
            'Apfel'

        You can use default value

            >>> taro: Japanese = Japanese.from_dict({
            ...     "name": 'taro'
            ... })  # doctest: +NORMALIZE_WHITESPACE
            >>> taro.name
            'taro'
            >>> taro.language
            'japanese'

        If you don't set `force_snake=False` explicitly, keys are transformed to snake case as following.

            >>> human: Human = Human.from_dict({
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
            >>> human.favorites[0].names_by_lang.get()["en"]
            'Apple'

        You can allow extra parameters (like ``hogehoge``) if you set `restrict=False`.

            >>> apple: Food = Food.from_dict({
            ...     "name": "Apple",
            ...     "hogehoge": "ooooooooooooooooooooo",
            ... }, restrict=False)
            >>> apple.to_dict()
            {'name': 'Apple'}

        You can prohibit extra parameters (like ``hogehoge``) if you set `restrict=True` (which is default).

            >>> human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "hogehoge1": "ooooooooooooooooooooo",
            ...     "hogehoge2": ["aaaaaaaaaaaaaaaaaa", "iiiiiiiiiiiiiiiii"],
            ...     "favorites": [
            ...         {"name": "Apple", "namesByLang": {"en": "Apple", "de": "Apfel"}},
            ...         {"name": "Orange"}
            ...     ]
            ... })  # doctest: +NORMALIZE_WHITESPACE
            Traceback (most recent call last):
                ...
            owlmixin.errors.UnknownPropertiesError:
            .        ∧,,_∧      ,___________________
                 ⊂ ( ･ω･ )つ-  <  Unknown properties error
               ／／/     /::/     `-------------------
               |::|/⊂ヽノ|::|」
            ／￣￣旦￣￣￣／|
            ＿＿＿＿＿＿／  | |
            |------ー----ー|／
            <BLANKLINE>
            `owlmixin.samples.Human` has unknown properties ['hogehoge1', 'hogehoge2']!!
            <BLANKLINE>
                * If you want to allow unknown properties, set `restrict=False`
                * If you want to disallow unknown properties, add `hogehoge1` and `hogehoge2` to owlmixin.samples.Human
            <BLANKLINE>

        If you specify wrong type...

            >>> human: Human = Human.from_dict({
            ...     "id": 1,
            ...     "name": "ichiro",
            ...     "favorites": ["apple", "orange"]
            ... })  # doctest: +NORMALIZE_WHITESPACE
            Traceback (most recent call last):
                ...
            owlmixin.errors.InvalidTypeError:
            .        ∧,,_∧      ,___________________
                 ⊂ ( ･ω･ )つ-  <  Invalid Type error
               ／／/     /::/     `-------------------
               |::|/⊂ヽノ|::|」
            ／￣￣旦￣￣￣／|
            ＿＿＿＿＿＿／  | |
            |------ー----ー|／
            <BLANKLINE>
            `owlmixin.samples.Human#favorites.0 = apple` doesn't match expected types.
            Expected type is one of ['Food', 'dict'], but actual type is `str`
            <BLANKLINE>
                * If you want to force cast, set `force_cast=True`
                * If you don't want to force cast, specify value which has correct type
            <BLANKLINE>

        If you don't specify required params... (ex. name

            >>> human: Human = Human.from_dict({
            ...     "id": 1
            ... })  # doctest: +NORMALIZE_WHITESPACE
            Traceback (most recent call last):
                ...
            owlmixin.errors.RequiredError:
            .        ∧,,_∧      ,___________________
                 ⊂ ( ･ω･ )つ-  <  Required error
               ／／/     /::/     `-------------------
               |::|/⊂ヽノ|::|」
            ／￣￣旦￣￣￣／|
            ＿＿＿＿＿＿／  | |
            |------ー----ー|／
            <BLANKLINE>
            `owlmixin.samples.Human#name: str` is empty!!
            <BLANKLINE>
                * If `name` is certainly required, specify anything.
                * If `name` is optional, change type from `str` to `TOption[str]`
            <BLANKLINE>
        """
        if isinstance(d, cls):
            return d

        instance: T = cls()
        d = util.replace_keys(d, {"self": "_self"}, force_snake_case)

        properties = cls.__annotations__.items()

        if restrict:
            assert_extra(properties, d, cls)

        for n, t in properties:
            f = cls._methods_dict.get(f'_{cls.__name__}___{n}')
            arg_v = f(d.get(n)) if f else d.get(n)
            def_v = getattr(instance, n, None)
            setattr(instance, n,
                    traverse(
                        type_=t,
                        name=n,
                        value=def_v if arg_v is None else arg_v,
                        cls=cls,
                        force_snake_case=force_snake_case,
                        force_cast=force_cast,
                        restrict=restrict
                    ))

        return instance

    @classmethod
    def from_optional_dict(cls, d: Optional[dict],
                           force_snake_case: bool=True,force_cast: bool=False, restrict: bool=True) -> TOption[T]:
        """From dict to optional instance.

        :param d: Dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dict(None).is_none()
            True
            >>> Human.from_optional_dict({}).get()  # doctest: +NORMALIZE_WHITESPACE
            Traceback (most recent call last):
                ...
            owlmixin.errors.RequiredError:
            .        ∧,,_∧      ,___________________
                 ⊂ ( ･ω･ )つ-  <  Required error
               ／／/     /::/     `-------------------
               |::|/⊂ヽノ|::|」
            ／￣￣旦￣￣￣／|
            ＿＿＿＿＿＿／  | |
            |------ー----ー|／
            <BLANKLINE>
            `owlmixin.samples.Human#id: int` is empty!!
            <BLANKLINE>
                * If `id` is certainly required, specify anything.
                * If `id` is optional, change type from `int` to `TOption[int]`
            <BLANKLINE>
        """
        return TOption(cls.from_dict(d,
                                     force_snake_case=force_snake_case,
                                     force_cast=force_cast,
                                     restrict=restrict) if d is not None else None)

    @classmethod
    def from_dicts(cls, ds: List[dict],
                   force_snake_case: bool=True, force_cast: bool=False, restrict: bool=True) -> TList[T]:
        """From list of dict to list of instance

        :param ds: List of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> humans: TList[Human] = Human.from_dicts([
            ...    {"id": 1, "name": "Tom", "favorites": [{"name": "Apple"}]},
            ...    {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ])
            >>> humans[0].name
            'Tom'
            >>> humans[1].name
            'John'
        """
        return TList([cls.from_dict(d,
                                    force_snake_case=force_snake_case,
                                    force_cast=force_cast,
                                    restrict=restrict) for d in ds])

    @classmethod
    def from_optional_dicts(cls, ds: Optional[List[dict]],
                            force_snake_case: bool=True, force_cast: bool=False, restrict: bool=True) -> TOption[TList[T]]:
        """From list of dict to optional list of instance.

        :param ds: List of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts(None).is_none()
            True
            >>> Human.from_optional_dicts([]).get()
            []
        """
        return TOption(cls.from_dicts(ds,
                                      force_snake_case=force_snake_case,
                                      force_cast=force_cast,
                                      restrict=restrict) if ds is not None else None)

    @classmethod
    def from_dicts_by_key(cls, ds: dict,
                          force_snake_case: bool=True, force_cast: bool=False, restrict: bool=True) -> TDict[T]:
        """From dict of dict to dict of instance

        :param ds: Dict of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Dict of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> humans_by_name: TDict[Human] = Human.from_dicts_by_key({
            ...    'Tom':  {"id": 1, "name": "Tom",  "favorites": [{"name": "Apple"}]},
            ...    'John': {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... })
            >>> humans_by_name['Tom'].name
            'Tom'
            >>> humans_by_name['John'].name
            'John'
        """
        return TDict({k: cls.from_dict(v,
                                       force_snake_case=force_snake_case,
                                       force_cast=force_cast,
                                       restrict=restrict) for k, v in ds.items()})

    @classmethod
    def from_optional_dicts_by_key(cls, ds: Optional[dict],
                                   force_snake_case=True, force_cast: bool=False, restrict: bool=True) -> TOption[TDict[T]]:
        """From dict of dict to optional dict of instance.

        :param ds: Dict of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Dict of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts_by_key(None).is_none()
            True
            >>> Human.from_optional_dicts_by_key({}).get()
            {}
        """
        return TOption(cls.from_dicts_by_key(ds,
                                             force_snake_case=force_snake_case,
                                             force_cast=force_cast,
                                             restrict=restrict) if ds is not None else None)

    @classmethod
    def from_json(cls, data: str, force_snake_case=True, force_cast: bool=False, restrict: bool=False) -> T:
        """From json string to instance

        :param data: Json string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> human: Human = Human.from_json('''{
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
            >>> human.favorites[0].names_by_lang.get()["de"]
            'Apfel'
        """
        return cls.from_dict(util.load_json(data),
                             force_snake_case=force_snake_case,
                             force_cast=force_cast,
                             restrict=restrict)

    @classmethod
    def from_jsonf(cls, fpath: str, encoding: str='utf8',
                   force_snake_case=True, force_cast: bool=False, restrict: bool=False) -> T:
        """From json file path to instance

        :param fpath: Json file path
        :param encoding: Json file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance
        """
        return cls.from_dict(util.load_jsonf(fpath, encoding),
                             force_snake_case=force_snake_case,
                             force_cast=force_cast,
                             restrict=restrict)

    @classmethod
    def from_json_to_list(cls, data: str,
                          force_snake_case=True, force_cast: bool=False, restrict: bool=False) -> TList[T]:
        """From json string to list of instance

        :param data: Json string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> humans: TList[Human] = Human.from_json_to_list('''[
            ...    {"id": 1, "name": "Tom",  "favorites": [{"name": "Apple"}]},
            ...    {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ]''')
            >>> humans[0].name
            'Tom'
            >>> humans[1].name
            'John'
        """
        return cls.from_dicts(util.load_json(data),
                              force_snake_case=force_snake_case,
                              force_cast=force_cast,
                              restrict=restrict)

    @classmethod
    def from_jsonf_to_list(cls, fpath: str, encoding: str='utf8',
                           force_snake_case=True, force_cast: bool=False, restrict: bool=False) -> TList[T]:
        """From json file path to list of instance

        :param fpath: Json file path
        :param encoding: Json file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance
        """
        return cls.from_dicts(util.load_jsonf(fpath, encoding),
                              force_snake_case=force_snake_case,
                              force_cast=force_cast,
                              restrict=restrict)

    @classmethod
    def from_yaml(cls, data: str, force_snake_case=True, force_cast: bool=False, restrict: bool=True) -> T:
        """From yaml string to instance

        :param data: Yaml string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> human: Human = Human.from_yaml('''
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
            >>> human.favorites[0].names_by_lang.get()["de"]
            'Apfel'
        """
        return cls.from_dict(util.load_yaml(data),
                             force_snake_case=force_snake_case,
                             force_cast=force_cast,
                             restrict=restrict)

    @classmethod
    def from_yamlf(cls, fpath: str, encoding: str='utf8',
                   force_snake_case=True, force_cast: bool=False, restrict: bool=True) -> T:
        """From yaml file path to instance

        :param fpath: Yaml file path
        :param encoding: Yaml file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance
        """
        return cls.from_dict(util.load_yamlf(fpath, encoding),
                             force_snake_case=force_snake_case,
                             force_cast=force_cast,
                             restrict=restrict)

    @classmethod
    def from_yaml_to_list(cls, data: str,
                          force_snake_case=True, force_cast: bool=False, restrict: bool=True) -> TList[T]:
        """From yaml string to list of instance

        :param data: Yaml string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> humans: TList[Human] = Human.from_yaml_to_list('''
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
        return cls.from_dicts(util.load_yaml(data),
                              force_snake_case=force_snake_case,
                              force_cast=force_cast,
                              restrict=restrict)

    @classmethod
    def from_yamlf_to_list(cls, fpath: str, encoding: str='utf8',
                           force_snake_case=True, force_cast: bool=False, restrict: bool=True) -> TList[T]:
        """From yaml file path to list of instance

        :param fpath: Yaml file path
        :param encoding: Yaml file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: List of instance
        """
        return cls.from_dicts(util.load_yamlf(fpath, encoding),
                              force_snake_case=force_snake_case,
                              force_cast=force_cast,
                              restrict=restrict)

    @classmethod
    def from_csvf(cls, fpath: str, fieldnames: Optional[Sequence[str]]=None, encoding: str='utf8',
                  force_snake_case: bool=True, restrict: bool=True) -> TList[T]:
        """From csv file path to list of instance

        :param fpath: Csv file path
        :param fieldnames: Specify csv header names if not included in the file
        :param encoding: Csv file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param restrict: Prohibit extra parameters if True
        :return: List of Instance
        """
        return cls.from_dicts(util.load_csvf(fpath, fieldnames, encoding),
                              force_snake_case=force_snake_case,
                              force_cast=True,
                              restrict=restrict)

    @classmethod
    def from_json_url(cls, url: str, force_snake_case=True, force_cast: bool=False, restrict: bool=False) -> T:
        """From url which returns json to instance

        :param url: Url which returns json
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :param restrict: Prohibit extra parameters if True
        :return: Instance
        """
        return cls.from_dict(util.load_json_url(url),
                             force_snake_case=force_snake_case,
                             force_cast=force_cast,
                             restrict=restrict)
