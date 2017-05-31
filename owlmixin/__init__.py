# coding: utf-8

from typing import TypeVar, List, Dict, Optional
import inspect

from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum, OwlObjectEnum
from owlmixin import util
from owlmixin.transformers import DictTransformer, JsonTransformer, YamlTransformer, traverse_dict, Option

__version__ = '1.2.0'

T = TypeVar('T', bound='OwlMixin')


def _is_generic(type):
    return hasattr(type, '__origin__')


def assert_none(value, type_, cls):
    assert value is not None, f'''
.        ∧,,_∧      ,___________________
     ⊂ ( ･ω･ )つ-  <  Required error!!  |
   ／／/     /::/     `-------------------
   |::|/⊂ヽノ|::|」
／￣￣旦￣￣￣／|
＿＿＿＿＿＿／  | |
|------ー----ー|／
    
* Type {type_} must not be None.
* Class: {cls}
    '''


def assert_type(value, type_):
    assert isinstance(value, type_), f'''
.        ∧,,_∧      ,_______________________
     ⊂ ( ･ω･ )つ-  <  Invalid Type error!!  |
   ／／/     /::/     `-----------------------
   |::|/⊂ヽノ|::|」
／￣￣旦￣￣￣／|
＿＿＿＿＿＿／  | |
|------ー----ー|／
    
* Expected: {type_}
* Actual: {type(value)}
* value: {value}
    '''


def traverse(type_, value, cls, force_snake_case: bool, force_cast: bool):
    if hasattr(type_, '__forward_arg__'):
        # XXX: Only if `_ForwardRef` includes myself
        type_ = cls
    if isinstance(value, type_):
        return value

    if not _is_generic(type_):
        assert_none(value, type_, cls)
        if issubclass(type_, OwlMixin):
            return type_.from_dict(value, force_snake_case)
        elif issubclass(type_, OwlEnum):
            return type_(value)
        elif issubclass(type_, OwlObjectEnum):
            return type_.from_symbol(value)
        else:
            if force_cast:
                return type_(value)
            else:
                assert_type(value, type_)
                return value

    o_type = type_.__origin__
    g_type = type_.__args__

    if o_type == TList:
        assert_none(value, type_, cls)
        assert_type(value, list)
        return TList([traverse(g_type[0], v, cls, force_snake_case, force_cast) for v in value])
    elif o_type == TDict:
        assert_none(value, type_, cls)
        assert_type(value, dict)
        return TDict({k: traverse(g_type[0], v, cls, force_snake_case, force_cast) for k, v in value.items()})
    elif o_type == Option:
        return Option(None) if value is None else Option(traverse(g_type[0], value, cls, force_snake_case, force_cast))
    else:
        assert False, f"This generics is not supported {o_type}"


class OwlMeta(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        cls._methods_dict = dict(inspect.getmembers(cls, inspect.ismethod))
        return cls


class OwlMixin(DictTransformer, JsonTransformer, YamlTransformer, metaclass=OwlMeta):
    @property
    def _dict(self):
        return self.__dict__

    @classmethod
    def from_dict(cls, d: dict, force_snake_case: bool=True, force_cast: bool=False) -> T:
        """From dict to instance

        :param d: Dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human, Food
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

        You can allow extra parameters (like ``hogehoge``).

            >>> apple: Food = Food.from_dict({
            ...     "name": "Apple",
            ...     "hogehoge": "ooooooooooooooooooooo",
            ... })
            >>> apple.to_dict()
            {'name': 'Apple'}

        FIXME:
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
        if isinstance(d, cls):
            return d

        instance: T = cls()
        d = util.replace_keys(d, {"self": "_self"}, force_snake_case)

        for n, t in cls.__annotations__.items():
            f = cls._methods_dict.get(f'_{cls.__name__}___{n}')
            setattr(instance, n, traverse(t, f(d.get(n)) if f else d.get(n), cls, force_snake_case, force_cast))

        return instance

    @classmethod
    def from_optional_dict(cls, d: Optional[dict], force_snake_case: bool=True, force_cast: bool=False) -> Option[T]:
        """From dict to optional instance.

        :param d: Dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dict(None).is_none()
            True
            >>> Human.from_optional_dict({}).get()
            Traceback (most recent call last):
                ...
            AssertionError:
            .        ∧,,_∧      ,___________________
                 ⊂ ( ･ω･ )つ-  <  Required error!!  |
               ／／/     /::/     `-------------------
               |::|/⊂ヽノ|::|」
            ／￣￣旦￣￣￣／|
            ＿＿＿＿＿＿／  | |
            |------ー----ー|／
            <BLANKLINE>
            * Type <class 'int'> must not be None.
            * Class: <class 'owlmixin.samples.Human'>
            <BLANKLINE>
        """
        return Option(cls.from_dict(d, force_snake_case, force_cast) if d is not None else None)

    @classmethod
    def from_dicts(cls, ds: List[dict], force_snake_case: bool=True, force_cast: bool=False) -> TList[T]:
        """From list of dict to list of instance

        :param ds: List of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return TList([cls.from_dict(d, force_snake_case, force_cast) for d in ds])

    @classmethod
    def from_optional_dicts(cls, ds: Optional[List[dict]], force_snake_case: bool=True, force_cast: bool=False) -> Option[TList[T]]:
        """From list of dict to optional list of instance.

        :param ds: List of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: List of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts(None).is_none()
            True
            >>> Human.from_optional_dicts([]).get()
            []
        """
        return Option(cls.from_dicts(ds, force_snake_case, force_cast) if ds is not None else None)

    @classmethod
    def from_dicts_by_key(cls, ds: dict, force_snake_case: bool=True, force_cast: bool=False) -> TDict[T]:
        """From dict of dict to dict of instance

        :param ds: Dict of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return TDict({k: cls.from_dict(v, force_snake_case, force_cast) for k, v in ds.items()})

    @classmethod
    def from_optional_dicts_by_key(cls, ds: Optional[dict], force_snake_case=True, force_cast: bool=False) -> Option[TDict[T]]:
        """From dict of dict to optional dict of instance.

        :param ds: Dict of dict
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Dict of instance

        Usage:

            >>> from owlmixin.samples import Human
            >>> Human.from_optional_dicts_by_key(None).is_none()
            True
            >>> Human.from_optional_dicts_by_key({}).get()
            {}
        """
        return Option(cls.from_dicts_by_key(ds, force_snake_case, force_cast) if ds is not None else None)

    @classmethod
    def from_json(cls, data: str, force_snake_case=True, force_cast: bool=False) -> T:
        """From json string to instance

        :param data: Json string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return cls.from_dict(util.load_json(data), force_snake_case, force_cast)

    @classmethod
    def from_jsonf(cls, fpath: str, encoding: str='utf8', force_snake_case=True, force_cast: bool=False) -> T:
        """From json file path to instance

        :param fpath: Json file path
        :param encoding: Json file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Instance
        """
        return cls.from_dict(util.load_jsonf(fpath, encoding), force_snake_case, force_cast)

    @classmethod
    def from_json_to_list(cls, data: str, force_snake_case=True, force_cast: bool=False) -> TList[T]:
        """From json string to list of instance

        :param data: Json string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return cls.from_dicts(util.load_json(data), force_snake_case, force_cast)

    @classmethod
    def from_jsonf_to_list(cls, fpath: str, encoding: str='utf8', force_snake_case=True, force_cast: bool=False) -> TList[T]:
        """From json file path to list of instance

        :param fpath: Json file path
        :param encoding: Json file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: List of instance
        """
        return cls.from_dicts(util.load_jsonf(fpath, encoding), force_snake_case, force_cast)

    @classmethod
    def from_yaml(cls, data: str, force_snake_case=True, force_cast: bool=False) -> T:
        """From yaml string to instance

        :param data: Yaml string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return cls.from_dict(util.load_yaml(data), force_snake_case, force_cast)

    @classmethod
    def from_yamlf(cls, fpath: str, encoding: str='utf8', force_snake_case=True, force_cast: bool=False) -> T:
        """From yaml file path to instance

        :param fpath: Yaml file path
        :param encoding: Yaml file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Instance
        """
        return cls.from_dict(util.load_yamlf(fpath, encoding), force_snake_case, force_cast)

    @classmethod
    def from_yaml_to_list(cls, data: str, force_snake_case=True, force_cast: bool=False) -> TList[T]:
        """From yaml string to list of instance

        :param data: Yaml string
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
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
        return cls.from_dicts(util.load_yaml(data), force_snake_case, force_cast)

    @classmethod
    def from_yamlf_to_list(cls, fpath: str, encoding: str='utf8', force_snake_case=True, force_cast: bool=False) -> TList[T]:
        """From yaml file path to list of instance

        :param fpath: Yaml file path
        :param encoding: Yaml file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: List of instance
        """
        return cls.from_dicts(util.load_yamlf(fpath, encoding), force_snake_case, force_cast)

    @classmethod
    def from_csvf(cls, fpath: str, fieldnames: Optional[List[str]]=None, encoding: str='utf8',
                  force_snake_case: bool=True) -> TList[T]:
        """From csv file path to list of instance

        :param fpath: Csv file path
        :param fieldnames: Specify csv header names if not included in the file
        :param encoding: Csv file encoding
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :return: List of Instance
        """
        return cls.from_dicts(util.load_csvf(fpath, fieldnames, encoding),
                              force_snake_case=force_snake_case, force_cast=True)

    @classmethod
    def from_json_url(cls, url: str, force_snake_case=True, force_cast: bool=False) -> T:
        """From url which returns json to instance

        :param url: Url which returns json
        :param force_snake_case: Keys are transformed to snake case in order to compliant PEP8 if True
        :param force_cast: Cast forcibly if True
        :return: Instance
        """
        return cls.from_dict(util.load_json_url(url), force_snake_case, force_cast)
