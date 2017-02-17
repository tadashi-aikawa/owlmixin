# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from . import util


def traverse(value, ignore_none=True):
    if isinstance(value, dict):
        return traverse_dict(value, ignore_none)
    elif isinstance(value, list):
        return traverse_list(value, ignore_none)
    elif isinstance(value, DictTransformable):
        return value.to_dict(ignore_none)
    else:
        return value


def traverse_dict(instance_dict, ignore_none):
    return {k: traverse(v, ignore_none) for
            k, v in instance_dict.items()
            if not (ignore_none and v is None)}


def traverse_list(instance_list, ignore_none):
    return [traverse(i, ignore_none) for i in instance_list]


class DictTransformable():
    """ `_to_dict()` can overridden
    """

    def _to_dict(self, ignore_none=True):
        return traverse(self, ignore_none)

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
        return self._to_dict(ignore_none)


class JsonTransformable():
    """ `_to_dict()` can overridden
    """

    def _to_dict(self, ignore_none=True):
        return traverse(self, ignore_none)

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
        return util.dump_json(self._to_dict(ignore_none), indent)

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


class YamlTransformable():
    """ `_to_dict()` can overridden
    """
    def _to_dict(self, ignore_none=True):
        return traverse(self, ignore_none)

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
        return util.dump_yaml(self._to_dict(ignore_none))
