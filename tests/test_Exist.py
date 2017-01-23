# coding: utf-8

from __future__ import division, absolute_import, unicode_literals

from owlmixin.util import O


class TestO:
    def test_then_not_none(self):
        assert O(1).then(lambda x: x + 1).or_(-1) == 2

    def test_then_zero(self):
        assert O(0).then(lambda x: x).or_(-1) == 0

    def test_then_none(self):
        assert O(None).then(lambda x: x + 1).or_("hoge") == "hoge"

    def test_then_empty_list(self):
        assert O([]).then(lambda x: x).or_("hoge") == []

    def test_then_empty_dict(self):
        assert O({}).then(lambda x: x).or_("hoge") == {}

    def test_then_or_none_not_none(self):
        assert O(1).then_or_none(lambda x: x + 1) == 2

    def test_then_or_none_zero(self):
        assert O(0).then_or_none(lambda x: x) == 0

    def test_then_or_none_none(self):
        assert O(None).then_or_none(lambda x: x + 1) is None

    def test_then_or_none_empty_list(self):
        assert O([]).then_or_none(lambda x: x) == []

    def test_then_or_none_empty_dict(self):
        assert O({}).then_or_none(lambda x: x) == {}
