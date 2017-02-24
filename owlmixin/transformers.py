# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from owlmixin import util


def traverse(value, ignore_none=True, force_value=False):
    if force_value and isinstance(value, ValueTransformer):
        return value.to_value()
    elif isinstance(value, dict):
        return traverse_dict(value, ignore_none, force_value)
    elif isinstance(value, list):
        return traverse_list(value, ignore_none, force_value)
    elif isinstance(value, DictTransformer):
        return value.to_dict(ignore_none, force_value)
    else:
        return value


def traverse_dict(instance_dict, ignore_none, force_value=False):
    return {k: traverse(v, ignore_none, force_value) for
            k, v in instance_dict.items()
            if not (ignore_none and v is None)}


def traverse_list(instance_list, ignore_none, force_value=False):
    return [traverse(i, ignore_none, force_value) for i in instance_list]


class ValueTransformer():
    def to_value(self):
        return str(self)


class DictTransformer():
    """ `@property _dict` can overridden
    """

    def to_dict(self, ignore_none=True, force_value=False):
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :param force_value: Transform to value using to_value (default: str()) of ValueTransformer which inherited if True
        :type force_value: bool
        :return: Dict
        :rtype: dict

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
        return traverse_dict(self._dict, ignore_none, force_value)


class DictsTransformer():
    """ `@property _dict` can overridden
    """

    def to_dicts(self, ignore_none=True, force_value=False):
        """From instance to dict

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :param force_value: Transform to value using to_value (default: str()) of ValueTransformer which inherited if True
        :type force_value: bool
        :return: List[Dict]
        :rtype: list[dict]

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

        You can include None properties by specifying None for ignore_none

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

        """
        return traverse_list(self, ignore_none, force_value)


class JsonTransformer():
    """ `@property _dict` can overridden
    """

    def to_json(self, indent=None, ignore_none=True):
        """From instance to json string

        :param indent: Number of indentation
        :type indent: Optional[int]
        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Json string
        :rtype: unicode

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
        return util.dump_json(traverse(self, ignore_none, force_value=True), indent)

    def to_pretty_json(self, ignore_none=True):
        """From instance to pretty json string

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Json string
        :rtype: unicode

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
        return self.to_json(4, ignore_none)


class YamlTransformer():
    """ `@property _dict` can overridden
    """

    def to_yaml(self, ignore_none=True):
        """From instance to yaml string

        :param ignore_none: Properties which is None are excluded if True
        :type ignore_none: bool
        :return: Yaml string
        :rtype: unicode

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
        return util.dump_yaml(traverse(self, ignore_none, force_value=True))


class CsvTransformer():
    """ `@property _dict` can overridden
    """

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
        return util.dump_csv(traverse(self, force_value=True), fieldnames, with_header, crlf)
