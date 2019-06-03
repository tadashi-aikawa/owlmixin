# coding: utf-8

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TDict, TList

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


class Address(OwlMixin):
    name: str


class Spot(OwlMixin):
    names: TList[str]
    address: TOption[Address]


class TestGet:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}
        assert Spot.from_dicts_by_key(d).get("a").get().to_dict() == {
            "names": ["spot1"],
            "address": {
                "name": "address1"
            }
        }

    def test_not_found(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}
        assert Spot.from_dicts_by_key(d).get("c").is_none()


class TestMap:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        # Sort for test
        assert sorted(Spot.from_dicts_by_key(d).map(lambda k, v: v.names), key=len) == [["spot1"], ["spot21", "spot22"]]


class TestMapValues:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        # Sort for test
        assert Spot.from_dicts_by_key(d).map_values(lambda v: len(v.names)).to_dict() == {"a": 1, "b": 2}


class TestMapValues2:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        # Sort for test
        assert Spot.from_dicts_by_key(d).map_values2(lambda k, v: f"len({k}.name) -> {len(v.names)}").to_dict() == {
            "a": "len(a.name) -> 1",
            "b": "len(b.name) -> 2"
        }


class TestFilter:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        assert Spot.from_dicts_by_key(d).filter(lambda k, v: v.address.get()).to_dicts() == [{
            "names": ["spot1"],
            "address": {
                "name": "address1"
            }
        }]


class TestReject:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        assert Spot.from_dicts_by_key(d).reject(lambda k, v: v.address.get()).to_dicts() == [{
            "names": ["spot21", "spot22"]
        }]


class TestSum:
    def test_normal(self):
        assert TDict({"a": 1, "b": 2, "c": 3}).sum() == 6


class TestSumBy:
    def test_normal(self):
        d = {"aaa": {"names": ["spot1"], "address": {"name": "address1"}}, "bb": {"names": ["spot21", "spot22"]}}

        assert Spot.from_dicts_by_key(d).sum_by(lambda k, v: len(k) * len(v.names)) == 7


class TestSize:
    def test_normal(self):
        d = {"a": {"names": ["spot1"], "address": {"name": "address1"}}, "b": {"names": ["spot21", "spot22"]}}

        assert Spot.from_dicts_by_key(d).size() == 2


class TestFind:
    def test_normal(self):
        d = {
            "a": {
                "names": ["spot1"],
                "address": {
                    "name": "address1"
                }
            },
            "b": {
                "names": ["spot21", "spot22"]
            },
            "c": {
                "names": ["spot31", "spot32", "spot33"]
            }
        }

        assert Spot.from_dicts_by_key(d).find(lambda k, v: len(v.names) == 2).get().to_dict(ignore_none=True) == {
            "names": ["spot21", "spot22"]
        }

    def test_not_found(self):
        d = {
            "a": {
                "names": ["spot1"],
                "address": {
                    "name": "address1"
                }
            },
            "b": {
                "names": ["spot21", "spot22"]
            },
            "c": {
                "names": ["spot31", "spot32"]
            }
        }

        assert Spot.from_dicts_by_key(d).find(lambda k, v: v.names == 3).is_none()


class TestToList:
    def test_normal(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        # Sort for test
        assert sorted(Spot.from_dicts_by_key(d).to_list().to_dicts(ignore_none=True), key=lambda x: x["names"][0]) == [{
            "names": ["spot1"]
        }, {
            "names": ["spot21", "spot22"]
        }, {
            "names": ["spot31", "spot32"]
        }]


class TestAll:
    def test_true(self):
        d = {"a": {"names": ["spot1"]}, "bb": {"names": ["spot21", "spot22"]}, "cc": {"names": ["spot31", "spot32"]}}

        assert Spot.from_dicts_by_key(d).all(lambda k, v: len(k) == len(v.names)) is True

    def test_false(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        assert Spot.from_dicts_by_key(d).all(lambda k, v: len(k) == len(v.names)) is False


class TestAny:
    def test_true(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        assert Spot.from_dicts_by_key(d).any(lambda k, v: len(k) == len(v.names)) is True

    def test_false(self):
        d = {
            "aaa": {
                "names": ["spot1"]
            },
            "bbb": {
                "names": ["spot21", "spot22"]
            },
            "ccc": {
                "names": ["spot31", "spot32"]
            }
        }

        assert Spot.from_dicts_by_key(d).any(lambda k, v: len(k) == len(v.names)) is False


class TestAssign:
    def test_normal(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        d2 = {"c": {"names": ["spot3"]}, "d": {"names": ["spot4"]}}

        spots_by_key: TDict[Spot] = Spot.from_dicts_by_key(d)
        actual: TDict[Spot] = spots_by_key.assign(d2)

        assert {
            "a": {
                "names": ["spot1"]
            },
            "b": {
                "names": ["spot21", "spot22"]
            },
            "c": {
                "names": ["spot3"]
            },
            "d": {
                "names": ["spot4"]
            }
        } == actual.to_dict()

        actual['a'] = None
        assert actual['a'] is None
        assert d['a'] is not None
        assert spots_by_key['a'] is not None


class TestPickBy:
    def test_normal(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        actual: TDict[Spot] = Spot.from_dicts_by_key(d).pick_by(lambda k, v: len(v.names) > 1 and k in ["a", "b"])

        assert {"b": {"names": ["spot21", "spot22"]}} == actual.to_dict()


class TestOmitBy:
    def test_normal(self):
        d = {"a": {"names": ["spot1"]}, "b": {"names": ["spot21", "spot22"]}, "c": {"names": ["spot31", "spot32"]}}

        actual: TDict[Spot] = Spot.from_dicts_by_key(d).omit_by(lambda k, v: len(v.names) > 1 and k in ["a", "b"])

        assert {"a": {"names": ["spot1"]}, "c": {"names": ["spot31", "spot32"]}} == actual.to_dict()
