# coding: utf-8

from owlmixin import OwlMixin
from owlmixin.owlenum import OwlObjectEnum


class Color(OwlObjectEnum):
    RED = (
        "red",
        {"japanese": "赤", "coloring": lambda m: "Red: " + m}
    )

    GREEN = (
        "green",
        {"japanese": "緑", "coloring": lambda m: "Green: " + m}
    )

    BLUE = (
        "blue",
        {"japanese": "青", "coloring": lambda m: "Blue: " + m}
    )

    @property
    def japanese(self):
        return self.object["japanese"]

    def coloring(self, message):
        return self.object["coloring"](message)


class Sample(OwlMixin):
    color: Color


class TestFromValue:
    def test_normal(self):
        assert Color.from_value("blue") is Color.BLUE


class TestProperty:
    def test_normal(self):
        assert Color.BLUE.japanese == "青"


class TestFunction:
    def test_normal(self):
        assert Color.BLUE.coloring("sky") == "Blue: sky"


class TestOwlMixin:
    def test_from_dict(self):
        ins: Sample = Sample.from_dict({"color": "blue"})
        assert ins.color == Color.BLUE

    def test_from_dict_includes_instance(self):
        ins: Sample = Sample.from_dict({"color": Color.BLUE})
        assert ins.color == Color.BLUE

    def test_to_dict(self):
        assert Sample.from_dict({"color": "blue"}).to_dict() == {
            "color": "blue"
        }
        assert Sample.from_dict({"color": "blue"}).to_dict(force_value=False) == {
            "color": Color.BLUE
        }

    def test_to_json(self):
        assert Sample.from_dict({"color": "blue"}).to_json() == '{"color": "blue"}'
