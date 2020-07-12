# coding: utf-8
# pylint: disable=no-self-use
import os

import pytest

from owlmixin import OwlMixin, TOption
from owlmixin.owlcollections import TList, TIterator


# noinspection DuplicatedCode
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


class TestToCsv:
    def test_normal(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name", "ruby"])
            == """
1,一郎,
2,二郎,じろう
""".lstrip()
        )
        assert d.to_csv(["id", "name", "ruby"]) == ""

    def test_ignore_extra_params(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name"])
            == """
1,一郎
2,二郎
""".lstrip()
        )
        assert d.to_csv(["id", "name"]) == ""

    def test_with_header(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name", "ruby"], with_header=True)
            == """
id,name,ruby
1,一郎,
2,二郎,じろう
""".lstrip()
        )
        assert (
            d.to_csv(["id", "name", "ruby"], with_header=True)
            == """
id,name,ruby
""".lstrip()
        )

    def test_with_space(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": " 一 郎 "}, {"id": 2, "name": " 二 郎 ", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name", "ruby"])
            == """
1, 一 郎 ,
2, 二 郎 ,じろう
""".lstrip()
        )
        assert d.to_csv(["id", "name", "ruby"]) == ""

    def test_crlf(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name", "ruby"], crlf=True)
            == """
1,一郎,\r
2,二郎,じろう\r
""".lstrip()
        )
        assert d.to_csv(["id", "name", "ruby"], crlf=True) == ""

    def test_tsv(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert (
            d.to_csv(["id", "name", "ruby"], tsv=True)
            == """
1\t一郎\t
2\t二郎\tじろう
""".lstrip()
        )
        assert d.to_csv(["id", "name", "ruby"], tsv=True) == ""

    def test_including_dict(self):
        d = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "address": {"name": "住所"}}]
        )

        assert (
            d.to_csv(["id", "name", "address"])
            == """
1,一郎,
2,二郎,{'name': '住所'}
""".lstrip()
        )
        assert d.to_csv(["id", "name", "address"]) == ""

    def test_including_list(self):
        d = Spot.from_iterable_dicts(
            [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        )

        assert (
            d.to_csv(["names", "address"])
            == """
['spot1'],{'name': 'address1'}
"['spot21','spot22']",
""".lstrip()
        )
        assert d.to_csv(["names", "address"]) == ""


class TestToCsvf:
    """
    Requirements: `from_csvf_to_iterator` are fine
    """

    def test_normal(self, tmpdir):
        origin = [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        it: TIterator[Human] = Human.from_iterable_dicts(origin)

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.csv")

        assert (
            it.to_csvf(
                fpath, fieldnames=["name", "id", "ruby"], encoding="euc-jp", with_header=False
            )
            == fpath
        )
        assert (
            Human.from_csvf_to_iterator(
                fpath, fieldnames=["name", "id", "ruby"], encoding="euc-jp"
            ).to_dicts()
            == origin
        )


class TestNextAt:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        assert Spot.from_iterable_dicts(d).next_at(1).get().to_dict() == {
            "names": ["spot21", "spot22"]
        }

    def test_not_found(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        assert Spot.from_iterable_dicts(d).next_at(2).is_none()


class TestForEach:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        ret = []
        assert Spot.from_iterable_dicts(d).for_each(lambda s: ret.append(s.names[0])) is None
        assert ret == ["spot1", "spot21"]


class TestMap:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).map(lambda s: s.names).to_list() == [
            ["spot1"],
            ["spot21", "spot22"],
        ]


class TestEMap:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).emap(lambda s, i: (i + 1, s.names)).to_list() == [
            (1, ["spot1"]),
            (2, ["spot21", "spot22"]),
        ]


class TestFlatten:
    def test_normal(self):
        assert TIterator([[1, 2], [3, 4]]).flatten().to_list() == [1, 2, 3, 4]


class TestFlatMap:
    def test_normal(self):
        ds = Human.from_iterable_dicts(
            [{"id": 1, "name": "一郎"}, {"id": 2, "name": "二郎", "ruby": "じろう"}]
        )

        assert ds.flat_map(lambda x: [x.id, x.name]).to_list() == [1, "一郎", 2, "二郎"]


class TestFilter:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).filter(lambda s: s.address.get()).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}}
        ]


class TestReject:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).reject(lambda s: s.address.get()).to_dicts() == [
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

        assert Spot.from_iterable_dicts(d).head().get().to_dict() == {
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

        assert Spot.from_iterable_dicts(d).take(3).to_dicts() == [
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
        ] == Spot.from_iterable_dicts(d).take_while(lambda x: x.names.size() > 1).to_dicts()


class TestTail:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_iterable_dicts(d).tail(3).to_dicts() == [
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

        assert Spot.from_iterable_dicts(d).uniq().to_dicts() == [
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

        assert Spot.from_iterable_dicts(d).uniq_by(lambda x: x.to_json()).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]


class TestPartition:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        rejected, fulfilled = Spot.from_iterable_dicts(d).partition(lambda s: s.address.get())

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

        assert Spot.from_iterable_dicts(d).group_by(lambda s: str(len(s.names))).to_dict(
            ignore_none=True
        ) == {
            "1": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot4"], "address": {"name": "address1"}},
            ],
            "2": [{"names": ["spot21", "spot22"]}, {"names": ["spot31", "spot32"]}],
        }

        assert Spot.from_iterable_dicts(d).group_by(lambda s: str(len(s.names)))["1"].map(
            lambda x: x.names
        ).to_dicts() == [["spot1"], ["spot4"]]


class TestKeyBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
            {"names": ["spot4"], "address": {"name": "address1"}},
        ]

        assert Spot.from_iterable_dicts(d).key_by(lambda s: str(len(s.names))).to_dict(
            ignore_none=True
        ) == {
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

        assert Spot.from_iterable_dicts(d).order_by(lambda x: len(x.names)).to_dicts() == [
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

        assert Spot.from_iterable_dicts(d).order_by(
            lambda x: len(x.names), reverse=True
        ).to_dicts() == [
            {"names": ["spot31", "spot32", "spot33", "spot34"]},
            {"names": ["spot21", "spot22", "spot23"]},
            {"names": ["spot41", "spot42"], "address": {"name": "address1"}},
            {"names": ["spot1"], "address": {"name": "address1"}},
        ]


class TestConcat:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        e = [{"names": ["spot31", "spot32"]}]

        assert Spot.from_iterable_dicts(d).concat(Spot.from_iterable_dicts(e)).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

    def test_first(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        e = [{"names": ["spot31", "spot32"]}]

        assert Spot.from_iterable_dicts(d).concat(
            Spot.from_iterable_dicts(e), first=True
        ).to_dicts() == [
            {"names": ["spot31", "spot32"]},
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ]


class TestReduce:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).reduce(lambda r, x: r + len(x.names), 100) == 103


class TestSum:
    def test_normal(self):
        assert TIterator([1, 2, 3]).sum() == 6


class TestSumBy:
    def test_normal(self):
        d = [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]

        assert Spot.from_iterable_dicts(d).sum_by(lambda x: len(x.names)) == 3


class TestCountBy:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).count_by(lambda x: len(x.names)) == {1: 1, 2: 2}


class TestJoin:
    def test_normal(self):
        assert TIterator(["a", "bc", "def"]).join("---") == "a---bc---def"

    def test_including_not_str(self):
        with pytest.raises(TypeError):
            TIterator(["1", 2, "3"]).join("---")


class TestFind:
    def test_normal(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32", "spot33"]},
        ]

        assert Spot.from_iterable_dicts(d).find(lambda x: len(x.names) == 2).get().to_dict(
            ignore_none=True
        ) == {"names": ["spot21", "spot22"]}

    def test_not_found(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).find(lambda x: len(x.names) == 3).is_none()


class TestAll:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).all(lambda x: x.names) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).all(lambda x: len(x.names) > 1) is False


class TestAny:
    def test_true(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).any(lambda x: len(x.names) > 1) is True

    def test_false(self):
        d = [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
            {"names": ["spot31", "spot32"]},
        ]

        assert Spot.from_iterable_dicts(d).any(lambda x: len(x.names) > 2) is False


class TestIntersection:
    def test_normal(self):
        assert TIterator([1, 2, 3, 4, 5]).intersection([2, 4, 6]).to_list() == [2, 4]

    def test_empty(self):
        assert TIterator([1, 2, 3, 4, 5]).intersection([7, 8]).to_list() == []


class TestNotIntersection:
    def test_normal(self):
        assert TIterator([1, 2, 3, 4, 5]).not_intersection([2, 4, 6]).to_list() == [1, 3, 5]

    def test_empty(self):
        assert TIterator([1, 2, 3, 4, 5]).not_intersection([1, 2, 3, 4, 5]).to_list() == []


class TestReverse:
    def test_normal(self):
        assert TIterator([1, 2, 3]).reverse().to_list() == [3, 2, 1]

    def test_empty(self):
        assert TIterator([]).reverse().to_list() == []
