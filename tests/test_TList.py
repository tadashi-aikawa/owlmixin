# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

import pytest
from typing import List, Optional

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList

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


class Human(OwlMixin):
    def __init__(self, id, name, ruby=None, address=None):
        self.id = id  # type: int
        self.name = name  # type: Text
        self.ruby = ruby  # type: Optional[Text]
        self.address = address  # type: Optional[Address]


class Test__Add__:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        e = [
            {"names": ["spot31", "spot32"]}
        ]

        sd = Spot.from_dicts(d)
        se = Spot.from_dicts(e)
        actual = sd + se

        assert sd.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]
        assert se.to_dicts() ==  [
            {"names": ["spot31", "spot32"]}
        ]

        assert isinstance(actual, TList)
        assert actual.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]


class TestToCsv:
    def test_normal(self):
        d = [
            {"id": 1, "name": "一郎"},
            {"id": 2, "name": "二郎", "ruby": "じろう"}
        ]

        assert Human.from_dicts(d).to_csv(["id", "name", "ruby"]) == """
1,一郎,
2,二郎,じろう
""".lstrip()

    def test_with_header(self):
        d = [
            {"id": 1, "name": "一郎"},
            {"id": 2, "name": "二郎", "ruby": "じろう"}
        ]

        assert Human.from_dicts(d).to_csv(["id", "name", "ruby"], with_header=True) == """
id,name,ruby
1,一郎,
2,二郎,じろう
""".lstrip()

    def test_with_space(self):
        d = [
            {"id": 1, "name": " 一 郎 "},
            {"id": 2, "name": " 二 郎 ", "ruby": "じろう"}
        ]

        assert Human.from_dicts(d).to_csv(["id", "name", "ruby"]) == """
1, 一 郎 ,
2, 二 郎 ,じろう
""".lstrip()

    def test_crlf(self):
        d = [
            {"id": 1, "name": "一郎"},
            {"id": 2, "name": "二郎", "ruby": "じろう"}
        ]

        assert Human.from_dicts(d).to_csv(["id", "name", "ruby"], crlf=True) == """
1,一郎,\r
2,二郎,じろう\r
""".lstrip()

    def test_including_dict(self):
        d = [
            {"id": 1, "name": "一郎"},
            {"id": 2, "name": "二郎", "address": {"name": "住所"}}
        ]

        assert Human.from_dicts(d).to_csv(["id", "name", "address"]) == """
1,一郎,
2,二郎,{'name': '住所'}
""".lstrip()

    def test_including_list(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).to_csv(["names", "address"]) == """
['spot1'],{'name': 'address1'}
"['spot21','spot22']",
""".lstrip()


class TestMap:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).map(lambda s: s.names) == [
            ["spot1"], ["spot21", "spot22"]
        ]


class TestEMap:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).emap(lambda s, i: (i+1, s.names)) == [
            (1, ["spot1"]), (2, ["spot21", "spot22"])
        ]


class TestFlatten:
    def test_normal(self):
        assert TList([[1, 2], [3, 4]]).flatten() == [1, 2, 3, 4]


class TestFlatMap:
    def test_normal(self):
        ds = Human.from_dicts([
            {"id": 1, "name": "一郎"},
            {"id": 2, "name": "二郎", "ruby": "じろう"}
        ])

        assert ds.flat_map(lambda x: [x.id, x.name]) == [1, '一郎', 2, '二郎']


class TestFilter:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).filter(lambda s: s.address).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestReject:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).reject(lambda s: s.address).to_dicts() == [
            {"names": ["spot21", "spot22"]}
        ]


class TestPartial:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        fulfilled, rejected = Spot.from_dicts(d).partial(lambda s: s.address)

        assert fulfilled.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]
        assert rejected.to_dicts() == [
            {"names": ["spot21", "spot22"]}
        ]


class TestGroupBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}}
        ]

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


class TestOrderBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}}
        ]

        assert Spot.from_dicts(d).order_by(lambda x: len(x.names)).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]}
        ]

    def test_reverse(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}}
        ]

        assert Spot.from_dicts(d).order_by(lambda x: len(x.names), reverse=True).to_dicts() == [
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestConcat:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        e = [
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).concat(Spot.from_dicts(e)).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

    def test_first(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        e = [
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).concat(Spot.from_dicts(e), first=True).to_dicts() == [
            {"names": ["spot31", "spot32"]},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

class TestReduce:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).reduce(lambda r, x: r+len(x.names), 100) == 103


class TestSum:
    def test_normal(self):
        assert TList([1, 2, 3]).sum() == 6


class TestSumBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).sum_by(lambda x: len(x.names)) == 3


class TestSize:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ]

        assert Spot.from_dicts(d).size() == 2


class TestJoin:
    def test_normal(self):
        assert TList(["a", "bc", "def"]).join("---") == "a---bc---def"

    def test_including_not_str(self):
        with pytest.raises(TypeError):
            TList(["1", 2, "3"]).join("---")


class TestFind:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32", "spot33"]}
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


class TestAll:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).all(lambda x: len(x.names) > 0) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).all(lambda x: len(x.names) > 1) is False


class TestAny:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).any(lambda x: len(x.names) > 1) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]}
        ]

        assert Spot.from_dicts(d).any(lambda x: len(x.names) > 2) is False


class TestIntersection:
    def test_normal(self):
        assert TList([1, 2, 3, 4, 5]).intersection([2, 4, 6]) == [2, 4]

    def test_empty(self):
        assert TList([1, 2, 3, 4, 5]).intersection([7, 8]) == []


class TestNotIntersection:
    def test_normal(self):
        assert TList([1, 2, 3, 4, 5]).not_intersection([2, 4, 6]) == [1, 3, 5]

    def test_empty(self):
        assert TList([1, 2, 3, 4, 5]).not_intersection([1, 2, 3, 4, 5]) == []
