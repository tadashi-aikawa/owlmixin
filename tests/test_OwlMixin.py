# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from typing import List, Optional
from mock import patch

import pytest

from owlmixin import OwlMixin
from owlmixin.collections import TDict, TList

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
    def __init__(self, id, name, favorite_spots, favorite_animal, friends_by_short_name=None):
        self.id = id  # type: int
        self.name = name  # type: Text
        self.favorite_spots = Spot.from_dicts(favorite_spots)  # type: TList[Spot]
        self.favorite_animal = Animal.from_dict(favorite_animal)  # type: Animal
        self.friends_by_short_name = Human.from_optional_dicts_by_key(friends_by_short_name)
        """:type: Optional[TDict[Text, Human]]"""


class Animal(OwlMixin):
    def __init__(self, id, name, is_big):
        self.id = int(id)  # type: int
        self.name = name  # type: Text
        # Unfortunately, this is number (0: True / 1:False)
        self.is_big = int(is_big) == 1  # type: bool

    @property
    def dict(self):
        # Override because of returning YES or NO on is_big
        return {
            "id": self.id,
            "name": self.name,
            "is_big": "YES" if self.is_big else "NO"
        }


SAMPLE_HUMAN = {
    "id": 1,
    "name": "メンバ1",
    "favorite_spots": [
        {
            "names": ["spot1"],
            "address": {
                "name": "address1"
            }
        },
        {"names": ["spot21", "spot22"]}
    ],
    "favorite_animal": {"id": 1, "name": "a dog", "is_big": 0},
    "friends_by_short_name": {
        "toshi": {
            "id": 100,
            "name": "TOSHIKI",
            "favorite_spots": [
                {"names": ["toshi_spot"]}
            ],
            "favorite_animal": {"id": 2, "name": "a cat", "is_big": 0}
        },
        "hide": {
            "id": 200,
            "name": "HIDEKI",
            "favorite_spots": [
                {"names": ["hide_spot"]}
            ],
            "favorite_animal": {"id": 3, "name": "a lion", "is_big": 1}
        }
    }
}
""":type: dict"""


class TestFromDict:
    def test_normal(self):
        r = Human.from_dict(SAMPLE_HUMAN)

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address.name == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

        assert r.favorite_animal.id == 1
        assert r.favorite_animal.name == "a dog"
        assert r.favorite_animal.is_big is False

        assert len(r.friends_by_short_name) == 2

        assert r.friends_by_short_name["toshi"].id == 100
        assert r.friends_by_short_name["toshi"].name == "TOSHIKI"
        assert len(r.friends_by_short_name["toshi"].favorite_spots) == 1
        assert r.friends_by_short_name["toshi"].favorite_spots[0].names[0] == "toshi_spot"
        assert r.friends_by_short_name["toshi"].favorite_animal.id == 2
        assert r.friends_by_short_name["toshi"].favorite_animal.name == "a cat"
        assert r.friends_by_short_name["toshi"].favorite_animal.is_big is False

        assert r.friends_by_short_name["hide"].id == 200
        assert r.friends_by_short_name["hide"].name == "HIDEKI"
        assert len(r.friends_by_short_name["hide"].favorite_spots) == 1
        assert r.friends_by_short_name["hide"].favorite_spots[0].names[0] == "hide_spot"
        assert r.friends_by_short_name["hide"].favorite_animal.id == 3
        assert r.friends_by_short_name["hide"].favorite_animal.name == "a lion"
        assert r.friends_by_short_name["hide"].favorite_animal.is_big is True

    def test_none(self):
        with pytest.raises(AttributeError):
            Human.from_dict(None)


class TestFromOptionalDict:
    def test_normal(self):
        r = Human.from_optional_dict(SAMPLE_HUMAN)

        assert r.id == 1
        assert r.name == "メンバ1"
        assert len(r.favorite_spots) == 2

        assert len(r.favorite_spots[0].names) == 1
        assert r.favorite_spots[0].names[0] == "spot1"
        assert r.favorite_spots[0].address.name == "address1"

        assert len(r.favorite_spots[1].names) == 2
        assert r.favorite_spots[1].names[0] == "spot21"
        assert r.favorite_spots[1].names[1] == "spot22"
        assert r.favorite_spots[1].address is None

        assert r.favorite_animal.id == 1
        assert r.favorite_animal.name == "a dog"
        assert r.favorite_animal.is_big is False

        assert len(r.friends_by_short_name) == 2

        assert r.friends_by_short_name["toshi"].id == 100
        assert r.friends_by_short_name["toshi"].name == "TOSHIKI"
        assert len(r.friends_by_short_name["toshi"].favorite_spots) == 1
        assert r.friends_by_short_name["toshi"].favorite_spots[0].names[0] == "toshi_spot"
        assert r.friends_by_short_name["toshi"].favorite_animal.id == 2
        assert r.friends_by_short_name["toshi"].favorite_animal.name == "a cat"
        assert r.friends_by_short_name["toshi"].favorite_animal.is_big is False

        assert r.friends_by_short_name["hide"].id == 200
        assert r.friends_by_short_name["hide"].name == "HIDEKI"
        assert len(r.friends_by_short_name["hide"].favorite_spots) == 1
        assert r.friends_by_short_name["hide"].favorite_spots[0].names[0] == "hide_spot"
        assert r.friends_by_short_name["hide"].favorite_animal.id == 3
        assert r.friends_by_short_name["hide"].favorite_animal.name == "a lion"
        assert r.friends_by_short_name["hide"].favorite_animal.is_big is True

    def test_none(self):
        assert Human.from_optional_dict(None) is None


class TestToDict:
    def test_normal(self):
        r = Human.from_dict(SAMPLE_HUMAN)
        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_spots": [
                        {"names": ["toshi_spot"]}
                    ],
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"}
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [
                        {"names": ["hide_spot"]}
                    ],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"}
                }
            }
        }

    def test_ignore_none_false(self):
        r = Human.from_dict(SAMPLE_HUMAN)
        assert r.to_dict(ignore_none=False) == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"], "address": None}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
            "friends_by_short_name": {
                "toshi": {
                    "id": 100,
                    "name": "TOSHIKI",
                    "favorite_spots": [
                        {"names": ["toshi_spot"], "address": None}
                    ],
                    "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"},
                    "friends_by_short_name": None
                },
                "hide": {
                    "id": 200,
                    "name": "HIDEKI",
                    "favorite_spots": [
                        {"names": ["hide_spot"], "address": None}
                    ],
                    "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"},
                    "friends_by_short_name": None
                }
            }
        }


class TestToDicts:
    def test_normal(self):
        spots = Human.from_dict(SAMPLE_HUMAN).favorite_spots
        assert spots.to_dicts() == [
            {
                "names": ["spot1"],
                "address": {
                    "name": "address1"
                }
            },
            {
                "names": ["spot21", "spot22"]
            }
        ]

    def test_ignore_none_false(self):
        spots = Human.from_dict(SAMPLE_HUMAN).favorite_spots
        assert spots.to_dicts(ignore_none=False) == [
            {
                "names": ["spot1"],
                "address": {
                    "name": "address1"
                }
            },
            {
                "names": ["spot21", "spot22"],
                "address": None
            }
        ]


class TestFromDicts:
    def test_normal(self):
        r = Spot.from_dicts(SAMPLE_HUMAN["favorite_spots"])

        assert len(r) == 2
        assert type(r) == TList
        assert r[0].to_dict() == {"names": ["spot1"], "address": {"name": "address1"}}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"]}


class TestFromOptionalDicts:
    def test_normal(self):
        r = Spot.from_optional_dicts(SAMPLE_HUMAN["favorite_spots"])

        assert len(r) == 2
        assert type(r) == TList
        assert r[0].to_dict() == {"names": ["spot1"], "address": {"name": "address1"}}
        assert r[1].to_dict() == {"names": ["spot21", "spot22"]}

    def test_none(self):
        assert Human.from_optional_dicts(None) is None


class TestFromDictsByKey:
    def test_normal(self):
        r = Human.from_dicts_by_key(SAMPLE_HUMAN["friends_by_short_name"])

        assert len(r) == 2
        assert type(r) == TDict
        assert r.to_dict() == {
            "toshi": {
                "id": 100,
                "name": "TOSHIKI",
                "favorite_spots": [
                    {"names": ["toshi_spot"]}
                ],
                "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"}
            },
            "hide": {
                "id": 200,
                "name": "HIDEKI",
                "favorite_spots": [
                    {"names": ["hide_spot"]}
                ],
                "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"}
            }
        }


class TestFromOptionalDictsByKey:
    def test_normal(self):
        r = Human.from_optional_dicts_by_key(SAMPLE_HUMAN["friends_by_short_name"])

        assert len(r) == 2
        assert type(r) == TDict
        assert r.to_dict() == {
            "toshi": {
                "id": 100,
                "name": "TOSHIKI",
                "favorite_spots": [
                    {"names": ["toshi_spot"]}
                ],
                "favorite_animal": {"id": 2, "name": "a cat", "is_big": "NO"}
            },
            "hide": {
                "id": 200,
                "name": "HIDEKI",
                "favorite_spots": [
                    {"names": ["hide_spot"]}
                ],
                "favorite_animal": {"id": 3, "name": "a lion", "is_big": "YES"}
            }
        }

    def test_none(self):
        assert Human.from_optional_dicts_by_key(None) is None


class TestFromCsvf:
    def test_normal_without_header(self):
        rs = Animal.from_csvf("tests/csv/animals_without_header.csv", ("id", "name", "is_big"))

        assert rs.to_dicts() == [
            {"id": 1, "name": "a 犬", "is_big": "NO"},
            {"id": 2, "name": "a 猫", "is_big": "NO"},
            {"id": 3, "name": "a ライオン", "is_big": "YES"},
        ]

    def test_normal_with_header(self):
        rs = Animal.from_csvf("tests/csv/animals_with_header.csv")

        assert rs.to_dicts() == [
            {"id": 1, "name": "a 犬", "is_big": "NO"},
            {"id": 2, "name": "a 猫", "is_big": "NO"},
            {"id": 3, "name": "a ライオン", "is_big": "YES"},
        ]

    def test_normal_separated_by_tab(self):
        rs = Animal.from_csvf("tests/csv/animals_tab_separated.csv", ("id", "name", "is_big"))

        assert rs.to_dicts() == [
            {"id": 1, "name": "a 犬", "is_big": "NO"},
            {"id": 2, "name": "a 猫", "is_big": "NO"},
            {"id": 3, "name": "a ライオン", "is_big": "YES"},
        ]

    def test_normal_shiftjis(self):
        rs = Animal.from_csvf("tests/csv/animals_shiftjis.csv", encoding='shift-jis')

        assert rs.to_dicts() == [
            {"id": 1, "name": "a 犬", "is_big": "NO"},
            {"id": 2, "name": "a 猫", "is_big": "NO"},
            {"id": 3, "name": "a ライオン", "is_big": "YES"},
        ]


@patch('owlmixin.util.load_json_url')
class TestFromJsonUrl:
    def test_normal(self, load_json_url):
        load_json_url.return_value = {
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": 0},
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

        assert Human.from_json_url("hogehoge").to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {
                    "names": ["spot1"],
                    "address": {"name": "address1"}
                },
                {
                    "names": ["spot21", "spot22"]
                }
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJson:
    def test_normal(self):
        r = Human.from_json("""{
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": 0},
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
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {
                    "names": ["spot1"],
                    "address": {"name": "address1"}
                },
                {
                    "names": ["spot21", "spot22"]
                }
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJsonf:
    def test_utf8(self):
        assert Human.from_jsonf('tests/json/human_utf8.json').to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {
                    "names": ["spot1"],
                    "address": {"name": "address1"}
                },
                {
                    "names": ["spot21", "spot22"]
                }
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }

    def test_shiftjis(self):
        assert Human.from_jsonf('tests/json/human_shiftjis.json', encoding='sjis').to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {
                    "names": ["spot1"],
                    "address": {"name": "address1"}
                },
                {
                    "names": ["spot21", "spot22"]
                }
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromJsonToList:
    def test_normal(self):
        r = Spot.from_json_to_list("""[
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["spot21", "spot22"]
            }
        ]
        """)

        assert r.to_dicts() == [
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["spot21", "spot22"]
            }
        ]


class TestFromJsonfToList:
    def test_utf8(self):
        assert Spot.from_jsonf_to_list('tests/json/spots_utf8.json').to_dicts() == [
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["スポット21", "スポット22"]
            }
        ]

    def test_shiftjis(self):
        assert Spot.from_jsonf_to_list('tests/json/spots_shiftjis.json', encoding='sjis').to_dicts() == [
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["スポット21", "スポット22"]
            }
        ]


class TestFromYaml:
    def test_normal(self):
        r = Human.from_yaml("""
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
              is_big: 0
        """)

        assert r.to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromYamlf:
    def test_utf8(self):
        assert Human.from_yamlf('tests/yaml/human_utf8.yaml').to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }

    def test_shiftjis(self):
        assert Human.from_yamlf('tests/yaml/human_shiftjis.yaml', encoding='sjis').to_dict() == {
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": "NO"},
        }


class TestFromYamlToList:
    def test_normal(self):
        r = Spot.from_yaml_to_list("""
            - address:
                name: address1
              names:
                - spot1
            - names:
                - spot21
                - spot22
        """)

        assert r.to_dicts() == [
            {
                "names": ["spot1"],
                "address": {"name": "address1"}
            },
            {
                "names": ["spot21", "spot22"]
            }
        ]


class TestFromYamlfToList:
    def test_utf8(self):
        assert Spot.from_yamlf_to_list('tests/yaml/spots_utf8.yaml').to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]}
        ]

    def test_shiftjis(self):
        assert Spot.from_yamlf_to_list('tests/yaml/spots_shiftjis.yaml', encoding='sjis').to_dicts() == [
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["スポット21", "スポット22"]}
        ]


class TestToJson:
    def test_normal_from_dict(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": 0}
        })

        assert r.to_json(ignore_none=True) == """{
"favorite_animal": {"id": 1,"is_big": "NO","name": "a dog"},
"favorite_spots": [{"address": {"name": "address1"},"names": ["spot1"]},{"names": ["spot21","spot22"]}],
"id": 1,
"name": "メンバ1"
}
""".replace("\n", "")

    def test_normal_from_list(self):
        r = Spot.from_dicts([
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ])

        assert r.to_json(ignore_none=True) == """[
{"address": {"name": "address1"},"names": ["spot1"]},{"names": ["spot21","spot22"]}
]
""".replace("\n", "")


class TestToPrettyJson:
    def test_normal(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": 1},
        })

        assert r.to_pretty_json(ignore_none=True) == """
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
    def test_normal_from_dict(self):
        r = Human.from_dict({
            "id": 1,
            "name": "メンバ1",
            "favorite_spots": [
                {"names": ["spot1"], "address": {"name": "address1"}},
                {"names": ["spot21", "spot22"]}
            ],
            "favorite_animal": {"id": 1, "name": "a dog", "is_big": 0}
        })

        assert r.to_yaml(ignore_none=True) == """
favorite_animal:
  id: 1
  is_big: 'NO'
  name: a dog
favorite_spots:
  - address:
      name: address1
    names:
      - spot1
  - names:
      - spot21
      - spot22
id: 1
name: メンバ1
""".lstrip()

    def test_normal_from_list(self):
        r = Spot.from_dicts([
            {"names": ["spot1"], "address": {"name": "address1"}},
            {"names": ["spot21", "spot22"]}
        ])

        assert r.to_yaml(ignore_none=True) == """
- address:
    name: address1
  names:
    - spot1
- names:
    - spot21
    - spot22
""".lstrip()
