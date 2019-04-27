# coding: utf-8

import pytest
from owlmixin import OwlMixin, TOption, TList, RequiredError


class Spot(OwlMixin):
    id: int
    name: str
    note: TOption[str]
    rank: TOption[int]
    children: TOption[TList['Spot']]


class TestTOption:
    def test_normal(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'Note1', 'rank': 1})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.get() == 'Note1'
        assert r.rank.get() == 1

    def test_note_is_empty(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.is_none()

    def test_note_is_empty_string(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': ''})
        assert r.id == 1
        assert r.name == 'Name1'
        # Fot `from_csvf`
        assert r.note.is_none()

    def test_note_is_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': None})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.note.is_none()

    def test_rank_is_zero(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'rank': 0})
        assert r.id == 1
        assert r.name == 'Name1'
        assert r.rank.get() == 0

    def test_name_is_empty(self):
        with pytest.raises(RequiredError) as e:
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
        with pytest.raises(RequiredError) as e:
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
        with pytest.raises(RequiredError) as e:
            Spot.from_dicts([
                {'id': 1, 'name': 'Name1'},
                {'id': 2}
            ])


class TestIsNone:
    def test_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert r.note.is_none()

    def test_not_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'note1'})
        assert not r.note.is_none()


class TestAny:
    def test_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert not r.note.any()

    def test_not_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'note1'})
        assert r.note.any()


class TestGetOr:
    def test_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert r.note.get_or('hoge') == 'hoge'

    def test_not_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'note1'})
        assert r.note.get_or('hoge') == 'note1'


class TestMap:
    def test_not_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1', 'note': 'note1'})
        assert r.note.map(lambda x: x * 2).get_or('hoge') == 'note1note1'

    def test_none(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})
        assert r.note.map(lambda x: x * 2).get_or('hoge') == 'hoge'


class TestFlatMap:
    def test_not_none(self):
        r: Spot = Spot.from_dict({
            'id': 1,
            'name': 'Name1',
            'note': 'note1',
            'children': [
                {
                    'id': 11,
                    'name': 'Name11',
                    'note': 'note11',
                }
            ]
        })
        assert r.children.flat_map(lambda x: x[0].note).get_or('hoge') == 'note11'

    def test_none(self):
        r: Spot = Spot.from_dict({
            'id': 1,
            'name': 'Name1',
            'note': 'note1',
        })
        assert r.children.flat_map(lambda x: x[0].note).get_or('hoge') == 'hoge'

    def test_none_deep(self):
        r: Spot = Spot.from_dict({
            'id': 1,
            'name': 'Name1',
            'note': 'note1',
            'children': [
                {
                    'id': 11,
                    'name': 'Name11',
                }
            ]
        })
        assert r.children.flat_map(lambda x: x[0].note).get_or('hoge') == 'hoge'


class TestNoExpressionError:
    def test(self):
        r: Spot = Spot.from_dict({'id': 1, 'name': 'Name1'})

        with pytest.raises(NotImplementedError):
            if r.note:
                pass
        with pytest.raises(NotImplementedError):
            if not r.note:
                pass
        with pytest.raises(NotImplementedError):
            if r.note == 'hoge':
                pass
        with pytest.raises(NotImplementedError):
            if r.note != 'hoge':
                pass
        with pytest.raises(NotImplementedError):
            if r.note > 0:
                pass
        with pytest.raises(NotImplementedError):
            if r.note >= 0:
                pass
        with pytest.raises(NotImplementedError):
            if r.note < 0:
                pass
        with pytest.raises(NotImplementedError):
            if r.note <= 0:
                pass
        with pytest.raises(NotImplementedError):
            if r.note in ['a', 'i', 'u']:
                pass

        # Want to add below...
        # with pytest.raises(NotImplementedError):
        #     if r.note is None:
        #         pass
        # with pytest.raises(NotImplementedError):
        #     if r.note is not None:
        #         pass
