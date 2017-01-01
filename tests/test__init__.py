# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import List, Optional

import pytest

from dictmixin import DictMixin, TList, TDict

# For python 3.5.0-3.5.1
try:
    from typing import Text
except ImportError:
    pass


class Human(DictMixin):
    def __init__(self, id, name, favorite_spots):
        self.id = id  # type: int
        self.name = name  # type: Text
        self.favorite_spots = Spot.from_dicts(favorite_spots)  # type: TList[Spot]


class Spot(DictMixin):
    def __init__(self, names, address=None):
        self.names = names  # type: List[Text]
        self.address = address  # type: Optional[Text]


class Animal(DictMixin):
    def __init__(self, id, name, is_big):
        self.id = int(id)  # type: int
        self.name = name  # type: Text
        self.is_big = is_big == "1"  # type: bool


class TestFromDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

    def test_none(self):
        with pytest.raises(AttributeError):
            Human.from_dict(None)


class TestFromOptionalDict:
    def test_normal(self):
        r = Human.from_optional_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

    def test_none(self):
        assert Human.from_optional_dict(None) is None


class TestToDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }

    def test_ignore_none(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_dict(ignore_none=True) == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        }


class TestFromDicts:
    def test_normal(self):
        r = Spot.from_dicts([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"]}
        ])

        assert len(r) == 2
        assert type(r) == TList
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": None}


class TestFromOptionalDicts:
    def test_normal(self):
        r = Spot.from_optional_dicts([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"]}
        ])

        assert len(r) == 2
        assert type(r) == TList
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": None}

    def test_none(self):
        assert Human.from_optional_dicts(None) is None


class TestFromDictsByKey:
    def test_normal(self):
        r = Spot.from_dicts_by_key({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"]}
        })

        assert len(r) == 2
        assert type(r) == TDict
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": None}


class TestFromOptionalDictsByKey:
    def test_normal(self):
        r = Spot.from_optional_dicts_by_key({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"]}
        })

        assert len(r) == 2
        assert type(r) == TDict
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": None}

    def test_none(self):
        assert Human.from_optional_dicts_by_key(None) is None


class TestFromCsv:
    def test_normal_without_header(self):
        rs = Animal.from_csv("tests/csv/animals_without_header.csv", ("id", "name", "is_big"))

        assert rs.to_dicts() == [
            {"id": 1, "name": "a dog", "is_big": False},
            {"id": 2, "name": "a cat", "is_big": False},
            {"id": 3, "name": "a lion", "is_big": True},
        ]

    def test_normal_with_header(self):
        rs = Animal.from_csv("tests/csv/animals_with_header.csv")

        assert rs.to_dicts() == [
            {"id": 1, "name": "a dog", "is_big": False},
            {"id": 2, "name": "a cat", "is_big": False},
            {"id": 3, "name": "a lion", "is_big": True},
        ]

    def test_normal_separated_by_tab(self):
        rs = Animal.from_csv("tests/csv/animals_tab_separated.csv", ("id", "name", "is_big"))

        assert rs.to_dicts() == [
            {"id": 1, "name": "a dog", "is_big": False},
            {"id": 2, "name": "a cat", "is_big": False},
            {"id": 3, "name": "a lion", "is_big": True},
        ]


class TestFromJson:
    def test_normal(self):
        r = Human.from_json("""{
            "favorite_spots": [
                {"address": "address1", "names": ["spot1"]},
                {"names": ["spot21", "spot22"]}
            ],
            "id": 1,
            "name": "メンバ1"
        }
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }


class TestFromYaml:
    def test_normal(self):
        r = Human.from_yaml("""
            id: 1
            name: "メンバ1"
            favorite_spots:
              - address: address1
                names:
                  - spot1
              - names:
                  - spot21
                  - spot22
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": None}
            ]
        }


class TestToJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_json() == """{
"favorite_spots": [{"address": "address1","names": ["spot1"]},{"address": null,"names": ["spot21","spot22"]}],
"id": 1,
"name": "メンバ1"
}
""".replace("\n", "")


class TestToPrettyJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_pretty_json() == """
{
    "favorite_spots": [
        {
            "address": "address1",
            "names": [
                "spot1"
            ]
        },
        {
            "address": null,
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


class TestToYaml:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"]}
            ]
        })

        assert r.to_yaml() == """
favorite_spots:
  - address: address1
    names:
      - spot1
  - address: null
    names:
      - spot21
      - spot22
id: 1
name: メンバ1
""".lstrip()


class TestTList:
    def test_to_dicts_normal(self):
        d = [
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"], "address": "address2"}
        ]

        assert d == Spot.from_dicts(d).to_dicts()


class TestTDict:
    def test_to_dicts_by_key_normal(self):
        d = {
            "a": {"names": ["spot1"], "address": "address1"},
            "b": {"names": ["spot21", "spot22"], "address": "address2"}
        }
        assert d == Spot.from_dicts_by_key(d).to_dict()
