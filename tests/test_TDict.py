# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import List, Optional

from owlmixin import OwlMixin

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


class Address(OwlMixin):
    def __init__(self, name):
        self.name = name  # type: Text


class Spot(OwlMixin):
    def __init__(self, names, address=None):
        self.names = names  # type: List[Text]
        self.address = Address.from_optional_dict(address)  # type: Optional[Address]


class TestMap:
    def test_normal(self):
        d = {
            "a": {"names": ["spot1"], "address": {"name": "address1"}},
            "b": {"names": ["spot21", "spot22"]}
        }

        assert Spot.from_dicts_by_key(d).map(lambda s: s.names) == [
            ["spot1"], ["spot21", "spot22"]
        ]


class TestFilter:
    def test_normal(self):
        d = {
            "a": {"names": ["spot1"], "address": {"name": "address1"}},
            "b": {"names": ["spot21", "spot22"]}
        }

        assert Spot.from_dicts_by_key(d).filter(lambda s: s.address).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestSize:
    def test_normal(self):
        d = {
            "a": {"names": ["spot1"], "address": {"name": "address1"}},
            "b": {"names": ["spot21", "spot22"]}
        }

        assert Spot.from_dicts_by_key(d).size() == 2


class TestFind:
    def test_normal(self):
        d = {
            "a": {"names": ["spot1"], "address": {"name": "address1"}},
            "b": {"names": ["spot21", "spot22"]},
            "c": {"names": ["spot31", "spot32"]}
        }

        assert Spot.from_dicts_by_key(d).find(lambda k, v: len(v.names) == 2).to_dict(ignore_none=True) == {
            "names": ["spot21", "spot22"]
        }

    def test_not_found(self):
        d = {
            "a": {"names": ["spot1"], "address": {"name": "address1"}},
            "b": {"names": ["spot21", "spot22"]},
            "c": {"names": ["spot31", "spot32"]}
        }

        assert Spot.from_dicts_by_key(d).find(lambda k, v: v.names == 3) is None
