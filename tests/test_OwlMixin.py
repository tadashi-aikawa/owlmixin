# coding: utf-8
# pylint: disable=no-self-use,too-many-lines

import os

import pytest
from mock import patch
from typing import Any

from owlmixin import OwlMixin, RequiredError
from owlmixin.owlcollections import TDict, TList
from owlmixin.owlenum import OwlEnum
from owlmixin.samples import Japanese
from owlmixin.transformers import TOption


class Color(OwlEnum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


class OnlyAny(OwlMixin):
    hoge: any  # type: ignore
    """ any is invalid """


class OnlyTypingAny(OwlMixin):
    hoge: Any


class ForwardRefType(OwlMixin):
    id: int
    address: "Address"
    address_optional: TOption["Address"]
    addresses: TList["Address"]
    addresses_optional: TOption[TList["Address"]]


class Paper(OwlMixin):
    name: str
    width: str
    height: int

    @classmethod
    def ___width(cls, v: int) -> str:
        return f"{v} px"


class Address(OwlMixin):
    name: str


class Spot(OwlMixin):
    names: TList[str]
    address: TOption[Address]
    color: TOption[Color]


class Animal(OwlMixin):
    id: int
    name: str
    is_big: bool

    @property
    def _dict(self):
        # Override because of returning YES or NO on is_big
        return {"id": self.id, "name": self.name, "is_big": "YES" if self.is_big else "NO"}


class Human(OwlMixin):
    id: int
    name: str
    favorite_spots: TList[Spot]
    favorite_animal: Animal
    friends_by_short_name: TOption[TDict["Human"]]


SAMPLE_HUMAN: dict = {
    "id": 1,
    "name": "メンバ1",
    "favorite_spots": [
        {"names": ["spot1"], "address": {"name": "address1"}},
        {"names": ["spot21", "spot22"], "color": "red"},
    ],
    "favorite_animal": {"id": 1, "name": "a dog", "is_big": False},
    "friends_by_short_name": {
        "toshi": {
            "id": 100,
            "name": "TOSHIKI",
            "favorite_spots": [{"names": ["toshi_spot"]}],
            "favorite_animal": {"id": 2, "name": "a cat", "is_big": False},
        },
        "hide": {
            "id": 200,
            "name": "HIDEKI",
            "favorite_spots": [{"names": ["hide_spot"]}],
            "favorite_animal": {"id": 3, "name": "a lion", "is_big": True},
        },
    },
}

SAMPLE_HUMAN2: dict = {
    "id": 1,
    "name": "メンバ1",
    "favorite_spots": [],
    "favorite_animal": {"id": 1, "name": "a dog", "is_big": False},
    "friends_by_short_name": {
        "toshi": {
            "id": 100,
            "name": "TOSHIKI",
            "favorite_spots": [],
            "favorite_animal": {"id": 2, "name": "a cat", "is_big": False},
        },
        "hide": {
            "id": 200,
            "name": "HIDEKI",
            "favorite_spots": [{"names": ["hide_spot"]}],
            "favorite_animal": {"id": 3, "name": "a lion", "is_big": True},
        },
    },
}


class TestFromDict:
    def test_normal(self):
        r: Human = Human.from_dict(SAMPLE_HUMAN)

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address.get().name == "address1"
        assert r.favorite_spots[0].color.is_none()

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address.is_none()
        assert r.favorite_spots[1].color.get() == Color.RED

        assert r.favorite_animal.id == 1
        assert r.favorite_animal.name == "a dog"
        assert r.favorite_animal.is_big is False

        assert len(r.friends_by_short_name.get()) == 2

        assert r.friends_by_short_name.get()["toshi"].id == 100
        assert r.friends_by_short_name.get()["toshi"].name == "TOSHIKI"
        assert len(r.friends_by_short_name.get()["toshi"].favorite_spots) == 1
        assert r.friends_by_short_name.get()["toshi"].favorite_spots[0].names[0] == "toshi_spot"
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.id == 2
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.name == "a cat"
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.is_big is False

        assert r.friends_by_short_name.get()["hide"].id == 200
        assert r.friends_by_short_name.get()["hide"].name == "HIDEKI"
        assert len(r.friends_by_short_name.get()["hide"].favorite_spots) == 1
        assert r.friends_by_short_name.get()["hide"].favorite_spots[0].names[0] == "hide_spot"
        assert r.friends_by_short_name.get()["hide"].favorite_animal.id == 3
        assert r.friends_by_short_name.get()["hide"].favorite_animal.name == "a lion"
        assert r.friends_by_short_name.get()["hide"].favorite_animal.is_big is True

    def test_from_instance(self):
        r: Human = Human.from_dict(SAMPLE_HUMAN)
        assert r.to_dict() == Human.from_dict(r).to_dict()

        assert (
            r.to_dict()
            == Human.from_dict(
                {
                    "id": r.id,
                    "name": r.name,
                    "favorite_spots": r.favorite_spots,
                    "favorite_animal": r.favorite_animal,
                    "friends_by_short_name": r.friends_by_short_name,
                }
            ).to_dict()
        )

    def test_from_dict_use_default_value(self):
        r: Japanese = Japanese.from_dict({"name": "taro"})
        assert r.name == "taro"
        assert r.language == "japanese"

    def test_from_dict_not_use_default_value(self):
        r: Japanese = Japanese.from_dict({"name": "tom", "language": "english"})
        assert r.name == "tom"
        assert r.language == "english"

    def test_from_dict_includes_any(self):
        r: OnlyAny = OnlyAny.from_dict({"hoge": {"huga": [1, 2, 3]}})
        assert r.hoge == {"huga": [1, 2, 3]}

    def test_from_dict_includes_typing_any(self):
        r: OnlyTypingAny = OnlyTypingAny.from_dict({"hoge": {"huga": [1, 2, 3]}})
        assert r.hoge == {"huga": [1, 2, 3]}

    def test_from_dict_includes_forwardref_type(self):
        r: ForwardRefType = ForwardRefType.from_dict(
            {"id": 1, "address": {"name": "address_name"}, "addresses": []}
        )
        assert r.id == 1
        assert r.address.name == "address_name"
        assert r.addresses == []

    def test_from_dict_includes_generic_forwardref_type(self):
        r: ForwardRefType = ForwardRefType.from_dict(
            {
                "id": 1,
                "address": {"name": "address_name"},
                "addresses": [{"name": "address_name1"}, {"name": "address_name2"}],
                "address_optional": {"name": "address_optional_name"},
                "addresses_optional": [{"name": "address_name1"}, {"name": "address_name2"}],
            }
        )
        assert r.id == 1
        assert r.address.name == "address_name"
        assert r.addresses.to_dicts() == [{"name": "address_name1"}, {"name": "address_name2"}]
        assert r.address_optional.get().name == "address_optional_name"
        assert r.addresses_optional.get().to_dicts() == [
            {"name": "address_name1"},
            {"name": "address_name2"},
        ]

    def test_none(self):
        with pytest.raises(AttributeError):
            Human.from_dict(None)


class TestFromOptionalDict:
    def test_normal(self):
        r: Human = Human.from_optional_dict(SAMPLE_HUMAN).get()

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address.get().name == "address1"
        assert r.favorite_spots[0].color.is_none()

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address.is_none()
        assert r.favorite_spots[1].color.get() == Color.RED

        assert r.favorite_animal.id == 1
        assert r.favorite_animal.name == "a dog"
        assert r.favorite_animal.is_big is False

        assert len(r.friends_by_short_name.get()) == 2

        assert r.friends_by_short_name.get()["toshi"].id == 100
        assert r.friends_by_short_name.get()["toshi"].name == "TOSHIKI"
        assert len(r.friends_by_short_name.get()["toshi"].favorite_spots) == 1
        assert r.friends_by_short_name.get()["toshi"].favorite_spots[0].names[0] == "toshi_spot"
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.id == 2
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.name == "a cat"
        assert r.friends_by_short_name.get()["toshi"].favorite_animal.is_big is False

        assert r.friends_by_short_name.get()["hide"].id == 200
        assert r.friends_by_short_name.get()["hide"].name == "HIDEKI"
        assert len(r.friends_by_short_name.get()["hide"].favorite_spots) == 1
        assert r.friends_by_short_name.get()["hide"].favorite_spots[0].names[0] == "hide_spot"
        assert r.friends_by_short_name.get()["hide"].favorite_animal.id == 3
        assert r.friends_by_short_name.get()["hide"].favorite_animal.name == "a lion"
        assert r.friends_by_short_name.get()["hide"].favorite_animal.is_big is True

    def test_none(self):
        assert Human.from_optional_dict(None).is_none()

    def test_empty(self):
        with pytest.raises(RequiredError):
            Human.from_optional_dict({})


class TestToDict:
    def test_normal(self):
        r: Human = Human.from_dict(SAMPLE_HUMAN)

        # Assert Option
        assert r.favorite_spots[0].address.get().name == "address1"
        assert r.favorite_spots[0].color.is_none()
        assert r.favorite_spots[1].address.is_none()
        assert r.favorite_spots[1].color.get() == Color.RED

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"], "color": "red"},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_spots": [{"names": ["toshi_spot"]}],
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [{"names": ["hide_spot"]}],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
                },
            },
        }

    def test_str_format(self):
        r: Human = Human.from_dict(SAMPLE_HUMAN)

        assert r.str_format("{id}: {name}") == "1: メンバ1"

    def test_ignore_none_false(self):
        r = Human.from_dict(SAMPLE_HUMAN)

        # Assert Option
        assert r.favorite_spots[0].address.get().name == "address1"
        assert r.favorite_spots[0].color.is_none()
        assert r.favorite_spots[1].address.is_none()
        assert r.favorite_spots[1].color.get() == Color.RED

        assert r.to_dict(ignore_none=False) == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}, "color": None},
                {"names": ["spot21", "spot22"], "address": None, "color": "red"},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_spots": [{"names": ["toshi_spot"], "address": None, "color": None}],
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
                    "friends_by_short_name": None,
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [{"names": ["hide_spot"], "address": None, "color": None}],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
                    "friends_by_short_name": None,
                },
            },
        }

    def test_ignore_empty_true(self):
        r = Human.from_dict(SAMPLE_HUMAN2)

        # Assert Option
        assert r.favorite_spots == []
        assert r.friends_by_short_name.get()["toshi"].favorite_spots == []
        assert r.friends_by_short_name.get()["hide"].favorite_spots != []

        expected = {
            "id": 1,
            "name": "メンバ1",
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [{"names": ["hide_spot"]}],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
                },
            },
        }

        assert expected == r.to_dict(ignore_empty=True)

    def test_force_value_false(self):
        r = Human.from_dict(SAMPLE_HUMAN)
        assert r.to_dict(force_value=False) == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"], "color": Color.RED},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_spots": [{"names": ["toshi_spot"]}],
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [{"names": ["hide_spot"]}],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
                },
            },
        }

    def test_string_value(self):
        assert TDict({"key": "value"}).to_dict() == {"key": "value"}

    def test_bytes_value(self):
        assert TDict({"key": b"value"}).to_dict() == {"key": b"value"}

    def test_tuple_value(self):
        assert TDict({"key": (1, 2, 3)}).to_dict() == {"key": (1, 2, 3)}

    def test_set_value(self):
        assert TDict({"key": {1, 2, 3}}).to_dict() == {"key": {1, 2, 3}}

    def test_iterator_value(self):
        assert TDict({"key": iter([1, 2, 3])}).to_dict() == {"key": [1, 2, 3]}


class TestToDicts:
    def test_normal(self):
        spots: TList[Spot] = Human.from_dict(SAMPLE_HUMAN).favorite_spots

        # Assert Option
        assert spots[0].color.is_none()
        assert spots[1].color.get() == Color.RED

        assert spots.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"], "color": "red"},
        ]

    def test_ignore_none_false(self):
        spots: TList[Spot] = Human.from_dict(SAMPLE_HUMAN).favorite_spots

        # Assert Option
        assert spots[0].color.is_none()
        assert spots[1].color.get() == Color.RED

        assert spots.to_dicts(ignore_none=False) == [
            {"names": ["spot1"], "address": {"name": "address1"}, "color": None},
            {"names": ["spot21", "spot22"], "address": None, "color": "red"},
        ]

    def test_ignore_empty_true(self):
        friends: TList[Human] = Human.from_dict(SAMPLE_HUMAN2).friends_by_short_name.get().to_list()

        # Assert Option
        assert friends[0].favorite_spots == []
        assert friends[1].favorite_spots != []

        expected = [
            {
                "id": 100,
                "name": "TOSHIKI",
                "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
            },
            {
                "id": 200,
                "name": "HIDEKI",
                "favorite_spots": [{"names": ["hide_spot"]}],
                "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
            },
        ]

        assert expected == friends.to_dicts(ignore_empty=True)

    def test_force_value_false(self):
        spots = Human.from_dict(SAMPLE_HUMAN).favorite_spots
        assert spots.to_dicts(force_value=False) == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"], "color": Color.RED},
        ]


class TestFromDicts:
    def test_normal(self):
        r = Spot.from_dicts(SAMPLE_HUMAN["favorite_spots"])

        assert len(r) == 2
        assert isinstance(r, TList)
        assert r[0].to_dict(force_value=False) == {
            "names": ["spot1"],
            "address": {"name": "address1"},
        }
        assert r[1].to_dict(force_value=False) == {
            "names": ["spot21", "spot22"],
            "color": Color.RED,
        }


class TestFromOptionalDicts:
    def test_normal(self):
        r: TOption[TList[Spot]] = Spot.from_optional_dicts(SAMPLE_HUMAN["favorite_spots"])

        assert len(r.get()) == 2
        assert isinstance(r.get(), TList)
        assert r.get()[0].to_dict(force_value=False) == {
            "names": ["spot1"],
            "address": {"name": "address1"},
        }
        assert r.get()[1].to_dict(force_value=False) == {
            "names": ["spot21", "spot22"],
            "color": Color.RED,
        }

    def test_none(self):
        assert Human.from_optional_dicts(None).is_none()

    def test_empty(self):
        r = Human.from_optional_dicts([])
        assert isinstance(r.get(), TList)
        assert not r.get()


class TestFromDictsByKey:
    def test_normal(self):
        r = Human.from_dicts_by_key(SAMPLE_HUMAN["friends_by_short_name"])

        assert len(r) == 2
        assert isinstance(r, TDict)
        assert r.to_dict() == {
            "toshi": {
                "id": 100,
                "name": "TOSHIKI",
                "favorite_spots": [{"names": ["toshi_spot"]}],
                "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
            },
            "hide": {
                "id": 200,
                "name": "HIDEKI",
                "favorite_spots": [{"names": ["hide_spot"]}],
                "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
            },
        }


class TestFromOptionalDictsByKey:
    def test_normal(self):
        r: TOption[TDict[Human]] = Human.from_optional_dicts_by_key(
            SAMPLE_HUMAN["friends_by_short_name"]
        )

        assert len(r.get()) == 2
        assert isinstance(r.get(), TDict)
        assert r.get().to_dict() == {
            "toshi": {
                "id": 100,
                "name": "TOSHIKI",
                "favorite_spots": [{"names": ["toshi_spot"]}],
                "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
            },
            "hide": {
                "id": 200,
                "name": "HIDEKI",
                "favorite_spots": [{"names": ["hide_spot"]}],
                "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
            },
        }

    def test_none(self):
        assert Human.from_optional_dicts_by_key(None).is_none()

    def test_empty(self):
        r = Human.from_optional_dicts_by_key({})
        assert isinstance(r.get(), TDict)
        assert not r.get()


class TestFromCsvfToList:
    def test_normal_without_header(self):
        rs = Paper.from_csvf_to_list(
            "tests/csv/papers_without_header.csv", ("name", "width", "height")
        )

        for _ in range(2):
            assert rs.to_dicts() == [
                {"name": "紙1", "width": "100 px", "height": 10},
                {"name": "紙2", "width": "200 px", "height": 20},
                {"name": "紙3", "width": "300 px", "height": 30},
            ]

    def test_normal_with_header(self):
        rs = Paper.from_csvf_to_list("tests/csv/papers_with_header.csv")

        for _ in range(2):
            assert rs.to_dicts() == [
                {"name": "紙1", "width": "100 px", "height": 10},
                {"name": "紙2", "width": "200 px", "height": 20},
                {"name": "紙3", "width": "300 px", "height": 30},
            ]

    def test_normal_separated_by_tab(self):
        rs = Paper.from_csvf_to_list(
            "tests/csv/papers_tab_separated.csv", ("name", "width", "height")
        )

        for _ in range(2):
            assert rs.to_dicts() == [
                {"name": "紙1", "width": "100 px", "height": 10},
                {"name": "紙2", "width": "200 px", "height": 20},
                {"name": "紙3", "width": "300 px", "height": 30},
            ]

    def test_normal_shiftjis(self):
        rs = Paper.from_csvf_to_list("tests/csv/papers_shiftjis.csv", encoding="shift-jis")

        for _ in range(2):
            assert rs.to_dicts() == [
                {"name": "紙1", "width": "100 px", "height": 10},
                {"name": "紙2", "width": "200 px", "height": 20},
                {"name": "紙3", "width": "300 px", "height": 30},
            ]


class TestFromCsvfToIterator:
    def test_normal_without_header(self):
        rs = Paper.from_csvf_to_iterator(
            "tests/csv/papers_without_header.csv", ("name", "width", "height")
        )

        assert rs.to_dicts() == [
            {"name": "紙1", "width": "100 px", "height": 10},
            {"name": "紙2", "width": "200 px", "height": 20},
            {"name": "紙3", "width": "300 px", "height": 30},
        ]
        assert rs.to_dicts() == []

    def test_normal_with_header(self):
        rs = Paper.from_csvf_to_iterator("tests/csv/papers_with_header.csv")

        assert rs.to_dicts() == [
            {"name": "紙1", "width": "100 px", "height": 10},
            {"name": "紙2", "width": "200 px", "height": 20},
            {"name": "紙3", "width": "300 px", "height": 30},
        ]
        assert rs.to_dicts() == []

    def test_normal_separated_by_tab(self):
        rs = Paper.from_csvf_to_iterator(
            "tests/csv/papers_tab_separated.csv", ("name", "width", "height")
        )

        assert rs.to_dicts() == [
            {"name": "紙1", "width": "100 px", "height": 10},
            {"name": "紙2", "width": "200 px", "height": 20},
            {"name": "紙3", "width": "300 px", "height": 30},
        ]
        assert rs.to_dicts() == []

    def test_normal_shiftjis(self):
        rs = Paper.from_csvf_to_iterator("tests/csv/papers_shiftjis.csv", encoding="shift-jis")

        assert rs.to_dicts() == [
            {"name": "紙1", "width": "100 px", "height": 10},
            {"name": "紙2", "width": "200 px", "height": 20},
            {"name": "紙3", "width": "300 px", "height": 30},
        ]
        assert rs.to_dicts() == []


@patch("owlmixin.util.load_json_url")
class TestFromJsonUrl:
    def test_normal(self, load_json_url):
        load_json_url.return_value = {
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": False},
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "id": 1,
            "name": "メンバ1",
        }

        assert Human.from_json_url("hogehoge").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJson:
    def test_normal(self):
        r = Human.from_json(
            """{
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": false},
            "favorite_spots": [
                {
                    "names": ["spot1"],
                    "address": {"name": "address1"}
                },
                {
                    "names": ["spot21", "spot22"]
                }
            ],
            "id": 1,
            "name": "メンバ1"
        }
        """
        )

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJsonf:
    def test_utf8(self):
        assert Human.from_jsonf("tests/json/human_utf8.json").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }

    def test_shiftjis(self):
        assert Human.from_jsonf("tests/json/human_shiftjis.json", encoding="sjis").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJsonToList:
    def test_normal(self):
        r = Spot.from_json_to_list(
            """[
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["spot21", "spot22"]
            }
        ]
        """
        )

        assert r.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ]


class TestFromJsonfToList:
    def test_utf8(self):
        assert Spot.from_jsonf_to_list("tests/json/spots_utf8.json").to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]},
        ]

    def test_shiftjis(self):
        assert Spot.from_jsonf_to_list(
            "tests/json/spots_shiftjis.json", encoding="sjis"
        ).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]},
        ]


class TestFromYaml:
    def test_normal(self):
        r = Human.from_yaml(
            """
            id: 1
            name: "メンバ1"
            favorite_spots:
              - address:
                  name: address1
                names:
                  - spot1
              - names:
                  - spot21
                  - spot22
            favorite_animal:
              id: 1
              name: "a dog"
              is_big: false
        """
        )

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromYamlf:
    def test_utf8(self):
        assert Human.from_yamlf("tests/yaml/human_utf8.yaml").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }

    def test_shiftjis(self):
        assert Human.from_yamlf("tests/yaml/human_shiftjis.yaml", encoding="sjis").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]},
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromYamlToList:
    def test_normal(self):
        r = Spot.from_yaml_to_list(
            """
            - address:
                name: address1
              names:
                - spot1
            - names:
                - spot21
                - spot22
        """
        )

        assert r.to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]},
        ]


class TestFromYamlfToList:
    def test_utf8(self):
        assert Spot.from_yamlf_to_list("tests/yaml/spots_utf8.yaml").to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]},
        ]

    def test_shiftjis(self):
        assert Spot.from_yamlf_to_list(
            "tests/yaml/spots_shiftjis.yaml", encoding="sjis"
        ).to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]},
        ]


class TestToJson:
    def test_normal_from_dict(self):
        r = Human.from_dict(
            {
                "id": 1,
                "name": "メンバ1",
                "favorite_spots": [
                    {"names": ["spot1"], "address": {"name": "address1"}},
                    {"names": ["spot21", "spot22"], "color": "red"},
                ],
                "favorite_animal": {"id": 1, "name": "a dog", "is_big": False},
            }
        )

        assert (
            r.to_json(ignore_none=True)
            == """{
"favorite_animal": {"id": 1,"is_big": "NO","name": "a dog"},
"favorite_spots": [{"address": {"name": "address1"},"names": ["spot1"]},{"color": "red","names": ["spot21","spot22"]}],
"id": 1,
"name": "メンバ1"
}
""".replace(
                "\n", ""
            )
        )

    def test_normal_from_list(self):
        r = Spot.from_dicts(
            [{"names": ["spot1"], "address": {"name": "address1"}}, {"names": ["spot21", "spot22"]}]
        )

        assert (
            r.to_json(ignore_none=True)
            == """[
{"address": {"name": "address1"},"names": ["spot1"]},{"names": ["spot21","spot22"]}
]
""".replace(
                "\n", ""
            )
        )

    def test_string_value(self):
        assert TDict({"key": "value"}).to_json() == '{"key": "value"}'

    def test_bytes_value(self):
        with pytest.raises(TypeError):
            assert TDict({"key": b"value"}).to_json()

    def test_tuple_value(self):
        assert TDict({"key": (1, 2, 3)}).to_json() == '{"key": [1,2,3]}'

    def test_set_value(self):
        with pytest.raises(TypeError):
            assert TDict({"key": {1, 2, 3}}).to_json()

    def test_iterator_value(self):
        assert TDict({"key": iter([1, 2, 3])}).to_json() == '{"key": [1,2,3]}'


class TestToJsonf:
    """
    Requirements: `from_jsonf` and `from_jsonf_to_list` are fine
    """

    def test_normal_from_dict(self, tmpdir):
        r = Spot.from_dict({"names": ["spot1"], "address": {"name": "あどれす"}})

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.json")

        assert r.to_jsonf(fpath, encoding="euc-jp", ignore_none=True) == fpath
        assert Spot.from_jsonf(fpath, encoding="euc-jp").to_dict() == r.to_dict()

    def test_normal_from_list(self, tmpdir):
        r = Spot.from_dicts(
            [
                {"names": ["spot1"], "address": {"name": "あどれす"}},
                {"names": ["spot21", "spot22"], "color": "red"},
            ]
        )

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.json")

        assert r.to_jsonf(fpath, encoding="sjis", ignore_none=True) == fpath
        assert Spot.from_jsonf_to_list(fpath, encoding="sjis").to_dicts() == r.to_dicts()


class TestToPrettyJson:
    def test_normal(self):
        r = Human.from_dict(
            {
                "id": 1,
                "name": "メンバ1",
                "favorite_spots": [
                    {"names": ["spot1"], "address": {"name": "address1"}},
                    {"names": ["spot21", "spot22"], "color": "red"},
                ],
                "favorite_animal": {"id": 1, "name": "a dog", "is_big": True},
            }
        )

        assert (
            r.to_pretty_json(ignore_none=True)
            == """
{
    "favorite_animal": {
        "id": 1,
        "is_big": "YES",
        "name": "a dog"
    },
    "favorite_spots": [
        {
            "address": {
                "name": "address1"
            },
            "names": [
                "spot1"
            ]
        },
        {
            "color": "red",
            "names": [
                "spot21",
                "spot22"
            ]
        }
    ],
    "id": 1,
    "name": "メンバ1"
}
""".strip()
        )


class TestToYaml:
    def test_normal_from_dict(self):
        r = Human.from_dict(
            {
                "id": 1,
                "name": "メンバ1",
                "favorite_spots": [
                    {"names": ["spot1"], "address": {"name": "address1"}},
                    {"names": ["spot21", "spot22"], "color": "red"},
                ],
                "favorite_animal": {"id": 1, "name": "a dog", "is_big": False},
            }
        )

        assert (
            r.to_yaml(ignore_none=True)
            == """
favorite_animal:
  id: 1
  is_big: 'NO'
  name: a dog
favorite_spots:
  - address:
      name: address1
    names:
      - spot1
  - color: red
    names:
      - spot21
      - spot22
id: 1
name: メンバ1
""".lstrip()
        )

    def test_normal_from_list(self):
        r = Spot.from_dicts(
            [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"], "color": "red"},
            ]
        )

        assert (
            r.to_yaml(ignore_none=True)
            == """
- address:
    name: address1
  names:
    - spot1
- color: red
  names:
    - spot21
    - spot22
""".lstrip()
        )


class TestToYamlf:
    """
    Requirements: `from_yamlf` and `from_yamlf_to_list` are fine
    """

    def test_normal_from_dict(self, tmpdir):
        r = Spot.from_dict({"names": ["spot1"], "address": {"name": "あどれす"}})

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.yml")

        assert r.to_yamlf(fpath, encoding="euc-jp", ignore_none=True) == fpath
        assert Spot.from_yamlf(fpath, encoding="euc-jp").to_dict() == r.to_dict()

    def test_normal_from_list(self, tmpdir):
        r = Spot.from_dicts(
            [
                {"names": ["spot1"], "address": {"name": "あどれす"}},
                {"names": ["spot21", "spot22"], "color": "red"},
            ]
        )

        fpath = os.path.join(tmpdir.mkdir("tmp").strpath, "test.yml")

        assert r.to_yamlf(fpath, encoding="sjis", ignore_none=True) == fpath
        assert Spot.from_yamlf_to_list(fpath, encoding="sjis").to_dicts() == r.to_dicts()
