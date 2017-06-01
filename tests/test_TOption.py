# coding: utf-8

import pytest
from owlmixin import OwlMixin, TOption, TList


class Spot(OwlMixin):
    id: int
    name: str
    note: TOption[str]
    children: TOption[TList['Spot']]


class TestTOption:
    def test_normal(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'Note1'})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.get() == 'Note1'

    def test_note_is_empty(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.is_none()

    def test_note_is_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': None})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.is_none()

    def test_name_is_empty(self):
        with pytest.raises(AttributeError) as e:
            Spot.from_dict({'id': 1})

    def test_has_children(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'children': [
            {'id': 11, 'name': 'Name11'},
            {'id': 12, 'name': 'Name12'}
        ]})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.children.get()[0].id == 11
        assert r.children.get()[0].name == 'Name11'
        assert r.children.get()[1].id == 12
        assert r.children.get()[1].name == 'Name12'

    def test_has_children_whose_name_is_empty(self):
        with pytest.raises(AttributeError) as e:
            Spot.from_dict({'id': 1, 'name': 'Name1', 'children': [
                {'id': 11, 'name': 'Name11'},
                {'id': 12}
            ]})

    def test_list_note_is_empty(self):
        r: TList[Spot] = Spot.from_dicts([
            {'id': 1, 'name': 'Name1'},
            {'id': 2, 'name': 'Name2', 'note': 'note2'}
        ])
        assert r.to_dicts() == [
            {'id': 1, 'name': 'Name1'},
            {'id': 2, 'name': 'Name2', 'note': 'note2'}
        ]

    def test_list_name_is_empty(self):
        with pytest.raises(AttributeError) as e:
            Spot.from_dicts([
                {'id': 1, 'name': 'Name1'},
                {'id': 2}
            ])
