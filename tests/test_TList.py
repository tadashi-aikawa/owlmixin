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
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).map(lambda s: s.names) == [
            ["spot1"], ["spot21", "spot22"]
        ]


class TestFilter:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).filter(lambda s: s.address).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestGroupBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}}
        ]

        print(Spot.from_dicts(d).group_by(lambda s: str(len(s.names))).to_dict(ignore_none=True))

        assert Spot.from_dicts(d).group_by(lambda s: str(len(s.names))).to_dict(ignore_none=True) == {
            "1": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot4"], "address": {"name": "address1"}}
            ],
            "2": [
                {"names": ["spot21", "spot22"]},
                {"names": ["spot31", "spot32"]}
            ]
        }


class TestReduce:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).reduce(lambda r, x: r+len(x.names), 100) == 103


class TestSize:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).size() == 2


class TestFind:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).find(lambda x: len(x.names) == 2).to_dict(ignore_none=True) == {
            "names": ["spot21", "spot22"]
        }

    def test_not_found(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).find(lambda x: len(x.names) == 3) is None
