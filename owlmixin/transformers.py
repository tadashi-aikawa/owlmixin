# coding: utf-8
from typing import List, Sequence

from owlmixin import util
from owlmixin.owloption import TOption


class ValueTransformer():
    def to_value(self, ignore_none, force_value):
        return str(self)


def is_ignore(v) -> bool:
    return v is None or (isinstance(v, TOption) and v.is_none())


def is_empty(v) -> bool:
    p = v.get() if (isinstance(v, TOption)) else v
    return (isinstance(v, list) and p == []) or (isinstance(v, dict) and p == {})


def traverse(value, ignore_none=True, force_value=False, ignore_empty=False):
    if force_value and isinstance(value, ValueTransformer):
        return value.to_value(ignore_none, force_value)
    elif isinstance(value, TOption):
        return traverse(value.get(), ignore_none, force_value, ignore_empty)
    elif isinstance(value, dict):
        return traverse_dict(value, ignore_none, force_value, ignore_empty)
    elif isinstance(value, list):
        return traverse_list(value, ignore_none, force_value, ignore_empty)
    elif isinstance(value, DictTransformer):
        return value.to_dict(ignore_none, force_value, ignore_empty)
    else:
        return value


def traverse_dict(instance_dict, ignore_none, force_value=False, ignore_empty=False):
    return {
        k: traverse(v, ignore_none, force_value, ignore_empty)
        for k, v in instance_dict.items() if not (ignore_empty and is_empty(v)) and not (ignore_none and is_ignore(v))
    }


def traverse_list(instance_list, ignore_none, force_value=False, ignore_empty=False):
    return [
        traverse(i, ignore_none, force_value, ignore_empty) for i in instance_list
        if not (ignore_none and is_ignore(i))
    ]


class DictTransformer():
    """ `@property _dict` can overridden
    """

    @property
    def _dict(self):
        return self.__dict__

    def str_format(self, format_: str) -> str:
        """From instance to str with formatting

        :param format_: format string
        :return: str

        Usage:

            >>> from owlmixin.samples import Human, Food
            >>> human_dict = {
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...     ]
            ... }
            >>> Human.from_dict(human_dict).str_format('{id}: {name}')
            '1: Tom'
        """
        return format_.format(**self.to_dict())

    def to_dict(self, ignore_none: bool = True, force_value: bool = True, ignore_empty: bool = False) -> dict:
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :param force_value: Transform to value using to_value (default: str()) of ValueTransformer which inherited if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Dict

        Usage:
            >>> from owlmixin.samples import Human, Food
            >>> human_dict = {
            ...     "id": 1,
            ...     "name": "Tom",
            ...     "favorites": [
            ...         {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...     ]
            ... }
            >>> Human.from_dict(human_dict).to_dict() == human_dict
            True

        You can include None properties by specifying False for ignore_none

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

        You can exclude Empty properties by specifying True for ignore_empty

            >>> f = Human.from_dict({"id": 1, "name": "Ichiro", "favorites": []}).to_dict()
            >>> f["favorites"]
            []
            >>> f = Human.from_dict({"id": 1, "name": "Ichiro", "favorites": []}).to_dict(ignore_empty=True)
            >>> "favorites" in f
            False

        """
        return traverse_dict(self._dict, ignore_none, force_value, ignore_empty)


class DictsTransformer():
    """ `@property _dict` can overridden
    """

    def to_dicts(self, ignore_none: bool = True, force_value: bool = True, ignore_empty: bool = False) -> List[dict]:
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :param force_value: Transform to value using to_value (default: str()) of ValueTransformer which inherited if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: List[Dict]

        Usage:

            >>> from owlmixin.samples import Human, Food
            >>> human_dicts = [
            ...     {
            ...         "id": 1,
            ...         "name": "Tom",
            ...         "favorites": [
            ...             {"name": "Apple", "names_by_lang": {"en": "Apple"}}
            ...         ]
            ...     },
            ...     {
            ...         "id": 2,
            ...         "name": "John",
            ...         "favorites": [
            ...             {"name": "Orange", "names_by_lang": {"en": "Orange"}}
            ...         ]
            ...     }
            ... ]
            >>> Human.from_dicts(human_dicts).to_dicts() == human_dicts
            True

        You can include None properties by specifying False for ignore_none

            >>> f = Food.from_dicts([{"name": "Apple"}]).to_dicts(ignore_none=False)
            >>> f[0]["name"]
            'Apple'
            >>> "names_by_lang" in f[0]
            True
            >>> f[0]["names_by_lang"]

        As default

            >>> f = Food.from_dicts([{"name": "Apple"}]).to_dicts()
            >>> f[0]["name"]
            'Apple'
            >>> "names_by_lang" in f[0]
            False

        You can exclude Empty properties by specifying True for ignore_empty

            >>> f = Human.from_dicts([{"id": 1, "name": "Ichiro", "favorites": []}]).to_dicts()
            >>> f[0]["favorites"]
            []
            >>> f = Human.from_dicts([{"id": 1, "name": "Ichiro", "favorites": []}]).to_dicts(ignore_empty=True)
            >>> "favorites" in f[0]
            False

        """
        return traverse_list(self, ignore_none, force_value, ignore_empty)


class JsonTransformer():
    """ `@property _dict` can overridden
    """

    def to_json(self, indent: int = None, ignore_none: bool = True, ignore_empty: bool = False) -> str:
        """From instance to json string

        :param indent: Number of indentation
        :param ignore_none: Properties which is None are excluded if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Json string

        Usage:

            >>> from owlmixin.samples import Human
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
        return util.dump_json(traverse(self, ignore_none, force_value=True, ignore_empty=ignore_empty), indent)

    def to_jsonf(
        self,
        fpath: str,
        encoding: str = 'utf8',
        indent: int = None,
        ignore_none: bool = True,
        ignore_empty: bool = False
    ) -> str:
        """From instance to json file

        :param fpath: Json file path
        :param encoding: Json file encoding
        :param indent: Number of indentation
        :param ignore_none: Properties which is None are excluded if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Json file path
        """
        return util.save_jsonf(
            traverse(self, ignore_none, force_value=True, ignore_empty=ignore_empty), fpath, encoding, indent
        )

    def to_pretty_json(self, ignore_none: bool = True, ignore_empty: bool = False) -> str:
        """From instance to pretty json string

        :param ignore_none: Properties which is None are excluded if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Json string

        Usage:

            >>> from owlmixin.samples import Human
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
        return self.to_json(4, ignore_none, ignore_empty)


class YamlTransformer():
    """ `@property _dict` can overridden
    """

    def to_yaml(self, ignore_none: bool = True, ignore_empty: bool = False) -> str:
        """From instance to yaml string

        :param ignore_none: Properties which is None are excluded if True
        :param ignore_empty: Properties which is empty are excluded if True
        :return: Yaml string

        Usage:

            >>> from owlmixin.samples import Human
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
        return util.dump_yaml(traverse(self, ignore_none, force_value=True, ignore_empty=ignore_empty))

    def to_yamlf(self, fpath: str, encoding: str = 'utf8', ignore_none: bool = True, ignore_empty: bool = False) -> str:
        """From instance to yaml file

        :param ignore_none: Properties which is None are excluded if True
        :param fpath: Yaml file path
        :param encoding: Yaml file encoding
        :return: Yaml file path
        """
        return util.save_yamlf(
            traverse(self, ignore_none, force_value=True, ignore_empty=ignore_empty), fpath, encoding
        )


class CsvTransformer():
    """ `@property _dict` can overridden
    """

    def to_csv(
        self, fieldnames: Sequence[str], with_header: bool = False, crlf: bool = False, tsv: bool = False
    ) -> str:
        """From sequence of text to csv string

        :param fieldnames: Order of columns by property name
        :param with_header: Add headers at the first line if True
        :param crlf: Add CRLF line break at the end of line if True, else add LF
        :param tsv: Use tabs as separator if True, else use comma
        :return: Csv string

        Usage:

            >>> from owlmixin.samples import Human
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
        return util.dump_csv(traverse(self, force_value=True), fieldnames, with_header, crlf, tsv)

    def to_csvf(
        self,
        fpath: str,
        fieldnames: Sequence[str],
        encoding: str = 'utf8',
        with_header: bool = False,
        crlf: bool = False,
        tsv: bool = False
    ) -> str:
        """From instance to yaml file

        :param fpath: Csv file path
        :param fieldnames: Order of columns by property name
        :param encoding: Csv file encoding
        :param with_header: Add headers at the first line if True
        :param crlf: Add CRLF line break at the end of line if True, else add LF
        :param tsv: Use tabs as separator if True, else use comma
        :return: Csv file path
        """
        return util.save_csvf(traverse(self, force_value=True), fieldnames, fpath, encoding, with_header, crlf, tsv)


class TableTransformer():
    """ `@property _dict` can overridden
    """

    def to_table(self, fieldnames: Sequence[str]) -> str:
        """From sequence of text to csv string

        :param fieldnames: Order of columns by property name
        :return: Table string

        Usage:

            >>> from owlmixin.samples import Human
            >>> humans = Human.from_dicts([
            ...     {"id": 1, "name": "Tom", "favorites": [{"name": "Apple"}]},
            ...     {"id": 2, "name": "John", "favorites": [{"name": "Orange"}]}
            ... ])
            >>> print(humans.to_table(fieldnames=['name', 'id', 'favorites']))
            | name | id  |      favorites       |
            | ---- | --- | -------------------- |
            | Tom  | 1   | [{'name': 'Apple'}]  |
            | John | 2   | [{'name': 'Orange'}] |
            <BLANKLINE>
        """
        return util.dump_table(traverse(self, force_value=True), fieldnames)
