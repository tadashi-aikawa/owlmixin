# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import List, Text
import pytest

from dictmixin import DictMixin, replace_keys


def del_trim(target):
    # type: (Text) -> Text
    return target.replace("\n", "").replace(" ", "")


class Human(DictMixin):
    def __init__(self, id, name, favorite_spots):
        # type: (int, Text, List[dict]) -> Human
        self.id = id
        self.name = name
        self.favorite_spots = Spot.from_dict2list(favorite_spots)  # type: List[Spot]


class Spot(DictMixin):
    def __init__(self, names, address):
        # type: (List[Text], Text) -> Spot
        self.names = names
        self.address = address


class TestReplaceKeys:
    def test_normal(self):
        keymap = {
            "self": "_self",
            "before": "after"
        }
        d = {
            "before": 1,
            "before2": 2,
            "self": 3,
            "self2": 4
        }

        expected = {
            "after": 1,
            "before2": 2,
            "_self": 3,
            "self2": 4
        }

        assert replace_keys(d, keymap) == expected


class TestFromDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
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
        assert r.favorite_spots[1].address == "address2"

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
                {"names": ["spot21", "spot22"], "address": "address2"}
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
        assert r.favorite_spots[1].address == "address2"

    def test_none(self):
        assert Human.from_optional_dict(None) is None


class TestFromDict2List:
    def test_normal(self):
        r = Spot.from_dict2list([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"], "address": "address2"}
        ])

        assert len(r) == 2
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": "address2"}


class TestFromOptionalDict2List:
    def test_normal(self):
        r = Spot.from_optional_dict2list([
            {"names": ["spot1"], "address": "address1"},
            {"names": ["spot21", "spot22"], "address": "address2"}
        ])

        assert len(r) == 2
        assert r[0].to_dict() == {"names": ["spot1"], "address": "address1"}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"], "address": "address2"}

    def test_none(self):
        assert Human.from_optional_dict2list(None) is None


class TestFromDict2Dict:
    def test_normal(self):
        r = Spot.from_dict2dict({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"], "address": "address2"}
        })

        assert len(r) == 2
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": "address2"}
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}


class TestFromOptionalDict2Dict:
    def test_normal(self):
        r = Spot.from_optional_dict2dict({
            "spot1": {"names": ["spot1"], "address": "address1"},
            "spot2": {"names": ["spot21", "spot22"], "address": "address2"}
        })

        assert len(r) == 2
        assert r["spot2"].to_dict() == {"names": ["spot21", "spot22"], "address": "address2"}
        assert r["spot1"].to_dict() == {"names": ["spot1"], "address": "address1"}

    def test_none(self):
        assert Human.from_optional_dict2dict(None) is None


class TestToDict:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
            ]
        })

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
            ]
        }


class TestFromJson:
    def test_normal(self):
        r = Human.from_json("""{
            "favorite_spots": [
                {"address": "address1", "names": ["spot1"]},
                {"address": "address2", "names": ["spot21", "spot22"]}
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
                {"names": ["spot21", "spot22"], "address": "address2"}
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
              - address: address2
                names:
                  - spot21
                  - spot22
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
            ]
        }


class TestToJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
            ]
        })

        assert del_trim(r.to_json()) == del_trim("""{
            "favorite_spots": [
                {"address": "address1", "names": ["spot1"]},
                {"address": "address2", "names": ["spot21", "spot22"]}
            ],
            "id": 1,
            "name": "メンバ1"
        }
        """)


class TestToPrettyJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": "address1"},
                {"names": ["spot21", "spot22"], "address": "address2"}
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
            "address": "address2",
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
                {"names": ["spot21", "spot22"], "address": "address2"}
            ]
        })

        assert r.to_yaml() == """
favorite_spots:
  - address: address1
    names:
      - spot1
  - address: address2
    names:
      - spot21
      - spot22
id: 1
name: メンバ1
""".lstrip()
