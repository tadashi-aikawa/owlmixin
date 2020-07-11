# coding: utf-8
# pylint: disable=no-self-use
import os

import pytest

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList


class Address(OwlMixin):
    name: str


class Spot(OwlMixin):
    names: TList[str]
    address: TOption[Address]


class Human(OwlMixin):
    id: int
    name: str
    ruby: TOption[str]
    address: TOption[Address]


class Test__Add__:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        e = [{"names": ["spot31", "spot32"]}]

        sd = Spot.from_dicts(d)
        se = Spot.from_dicts(e)
        actual = sd + se

        assert sd.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ]
        assert se.to_dicts() == [{"names": ["spot31", "spot32"]}]

        assert isinstance(actual, TList)
        assert actual.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

    def test_exchange_rule(self):
        assert [1, 2] == TList([1]) + TList([2])
        assert [1, 2] == [1] + TList([2])
        assert [1, 2] == TList([1]) + [2]


class TestToCsv:
    def test_normal(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "ruby"])
            == """
1,一郎,
2,二郎,じろう
""".lstrip()
        )

    def test_ignore_extra_params(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name"])
            == """
1,一郎
2,二郎
""".lstrip()
        )

    def test_with_header(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "ruby"], with_header=True)
            == """
id,name,ruby
1,一郎,
2,二郎,じろう
""".lstrip()
        )

    def test_with_space(self):
        d = [{"id": 1, "name": " 一 郎 "}, {"id": 2, "name": " 二 郎 ", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "ruby"])
            == """
1, 一 郎 ,
2, 二 郎 ,じろう
""".lstrip()
        )

    def test_crlf(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "ruby"], crlf=True)
            == """
1,一郎,\r
2,二郎,じろう\r
""".lstrip()
        )

    def test_tsv(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "ruby"], tsv=True)
            == """
1\t一郎\t
2\t二郎\tじろう
""".lstrip()
        )

    def test_including_dict(self):
        d = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "address": {"name": "住所"}}]

        assert (
            Human.from_dicts(d).to_csv(["id", "name", "address"])
            == """
1,一郎,
2,二郎,{'name': '住所'}
""".lstrip()
        )

    def test_including_list(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert (
            Spot.from_dicts(d).to_csv(["names", "address"])
            == """
['spot1'],{'name': 'address1'}
"['spot21','spot22']",
""".lstrip()
        )


class TestToCsvf:
    """
    Requirements: `from_csvf_to_list` are fine
    """

    def test_normal(self, tmpdir):
        r: TList[Human] = Human.from_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.csv")

        assert (
            r.to_csvf(
                fpath, fieldnames=["name", "id", "ruby"], encoding="euc-jp", with_header=False
            )
            == fpath
        )
        assert (
            Human.from_csvf_to_list(
                fpath, fieldnames=["name", "id", "ruby"], encoding="euc-jp"
            ).to_dicts()
            == r.to_dicts()
        )


class TestGet:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        assert Spot.from_dicts(d).get(1).get().to_dict() == {"names": ["spot21", "spot22"]}

    def test_not_found(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        assert Spot.from_dicts(d).get(2).is_none()


class TestForEach:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        ret = []
        assert Spot.from_dicts(d).for_each(lambda s: ret.append(s.names[0])) is None
        assert ret == ["spot1", "spot21"]


class TestMap:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).map(lambda s: s.names) == [["spot1"], ["spot21", "spot22"]]


class TestEMap:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).emap(lambda s, i: (i + 1, s.names)) == [
            (1, ["spot1"]),
            (2, ["spot21", "spot22"]),
        ]


class TestFlatten:
    def test_normal(self):
        assert TList([[1, 2], [3, 4]]).flatten() == [1, 2, 3, 4]


class TestFlatMap:
    def test_normal(self):
        ds = Human.from_dicts([{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}])

        assert ds.flat_map(lambda x: [x.id, x.name]) == [1, "一郎", 2, "二郎"]


class TestFilter:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).filter(lambda s: s.address.get()).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestReject:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).reject(lambda s: s.address.get()).to_dicts() == [
            {"names": ["spot21", "spot22"]}
        ]


class TestHead:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).head().get().to_dict() == {
            "names": ["spot1"],
            "address": {"name": "address1"},
        }


class TestTake:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).take(3).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]


class TestTakeWhile:
    def test_normal(self):
        d = [
            {"names": ["spot11", "spot12"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
        ]

        assert [
            {"names": ["spot11", "spot12"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ] == Spot.from_dicts(d).take_while(lambda x: x.names.size() > 1).to_dicts()


class TestTail:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).tail(3).to_dicts() == [
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]


class TestUniq:
    def test_normal(self):
        """ Don't forget `d[0] != d[1]`
        """
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).uniq().to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]


class TestUniqBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).uniq_by(lambda x: x.to_json()).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]


class TestPartition:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        rejected, fulfilled = Spot.from_dicts(d).partition(lambda s: s.address.get())

        assert fulfilled.to_dicts() == [{"names": ["spot1"], "address": {"name": "address1"}}]
        assert rejected.to_dicts() == [{"names": ["spot21", "spot22"]}]


class TestGroupBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).group_by(lambda s: str(len(s.names))).to_dict(
            ignore_none=True
        ) == {
            "1": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot4"], "address": {"name": "address1"}},
            ],
            "2": [{"names": ["spot21", "spot22"]}, {"names": ["spot31", "spot32"]}],
        }


class TestKeyBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).key_by(lambda s: str(len(s.names))).to_dict(ignore_none=True) == {
            "1": {"names": ["spot4"], "address": {"name": "address1"}},
            "2": {"names": ["spot31", "spot32"]},
        }


class TestOrderBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).order_by(lambda x: len(x.names)).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
        ]

    def test_reverse(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
        ]

        assert Spot.from_dicts(d).order_by(lambda x: len(x.names), reverse=True).to_dicts() == [
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}},
        ]


class TestConcat:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        e = [{"names": ["spot31", "spot32"]}]

        assert Spot.from_dicts(d).concat(Spot.from_dicts(e)).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

    def test_first(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        e = [{"names": ["spot31", "spot32"]}]

        assert Spot.from_dicts(d).concat(Spot.from_dicts(e), first=True).to_dicts() == [
            {"names": ["spot31", "spot32"]},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ]


class TestReduce:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).reduce(lambda r, x: r + len(x.names), 100) == 103


class TestSum:
    def test_normal(self):
        assert TList([1, 2, 3]).sum() == 6


class TestSumBy:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_dicts(d).sum_by(lambda x: len(x.names)) == 3


class TestCountBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_dicts(d).count_by(lambda x: len(x.names)) == {1: 1, 2: 2}


class TestSize:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

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
            {"names": ["spot31", "spot32", "spot33"]},
        ]

        assert Spot.from_dicts(d).find(lambda x: len(x.names) == 2).get().to_dict(
            ignore_none=True
        ) == {"names": ["spot21", "spot22"]}

    def test_not_found(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_dicts(d).find(lambda x: len(x.names) == 3).is_none()


class TestAll:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_dicts(d).all(lambda x: x.names) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_dicts(d).all(lambda x: len(x.names) > 1) is False


class TestAny:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_dicts(d).any(lambda x: len(x.names) > 1) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
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


class TestReverse:
    def test_normal(self):
        assert TList([1, 2, 3]).reverse() == [3, 2, 1]

    def test_empty(self):
        assert TList([]).reverse() == []
