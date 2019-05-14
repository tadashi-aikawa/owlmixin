# coding: utf-8

from typing import Generic, TypeVar, Callable

T = TypeVar('T')
U = TypeVar('U')


class TOption(Generic[T]):
    def __init__(self, value):
        self.value = value

    def get(self) -> T:
        """
        Usage:

            >>> TOption(3).get()
            3
            >>> TOption(0).get()
            0
            >>> TOption(None).get()
        """
        return self.value

    def get_or(self, default: T) -> T:
        """
        Usage:

            >>> TOption(3).get_or(999)
            3
            >>> TOption(0).get_or(999)
            0
            >>> TOption(None).get_or(999)
            999
        """
        return default if self.value is None else self.value

    def is_none(self) -> bool:
        """
        Usage:

            >>> TOption(3).is_none()
            False
            >>> TOption(0).is_none()
            False
            >>> TOption(None).is_none()
            True
        """
        return self.value is None

    def any(self) -> bool:
        """
        Usage:

            >>> TOption(3).any()
            True
            >>> TOption(0).any()
            True
            >>> TOption(None).any()
            False
        """
        return self.value is not None

    def map(self, func: Callable[[T], U]) -> 'TOption[U]':
        """
        Usage:

            >>> TOption(3).map(lambda x: x+1).get()
            4
            >>> TOption(None).map(lambda x: x+1).get_or(999)
            999
        """
        return self if self.is_none() else TOption(func(self.value))

    def flat_map(self, func: Callable[[T], 'TOption[U]']) -> 'TOption[U]':
        """
        Usage:

            >>> TOption(3).flat_map(lambda x: TOption(str(x+1))).get()
            '4'
            >>> TOption(3).flat_map(lambda x: TOption(None)).get_or("none")
            'none'
            >>> TOption(None).flat_map(lambda x: TOption(str(x+1))).get_or("none")
            'none'
        """
        return self if self.is_none() else TOption(func(self.value).get())

    def __repr__(self):
        return f'Option --> {self.get()}'

    def __raise_no_conditional_expression(self, expression_name):
        raise NotImplementedError(f'No expression `{expression_name}` in TOption instance')

    def __add__(self, other):
        self.__raise_no_conditional_expression('__add__')

    def __and__(self, other):
        self.__raise_no_conditional_expression('__and__')

    def __bool__(self):
        self.__raise_no_conditional_expression('__bool__')

    def __contains__(self, item):
        self.__raise_no_conditional_expression('__contains__')

    def __delete__(self, instance):
        self.__raise_no_conditional_expression('__delete__')

    def __eq__(self, other):
        self.__raise_no_conditional_expression('__eq__')

    def __format__(self, format_spec):
        self.__raise_no_conditional_expression('__format__')

    def __float__(self):
        self.__raise_no_conditional_expression('__float__')

    def __ge__(self, other):
        self.__raise_no_conditional_expression('__ge__')

    def __gt__(self, other):
        self.__raise_no_conditional_expression('__gt__')

    def __int__(self):
        self.__raise_no_conditional_expression('__int__')

    def __le__(self, other):
        self.__raise_no_conditional_expression('__le__')

    def __len__(self):
        self.__raise_no_conditional_expression('__len__')

    def __lt__(self, other):
        self.__raise_no_conditional_expression('__lt__')

    def __mul__(self, other):
        self.__raise_no_conditional_expression('__mul__')

    def __mod__(self, other):
        self.__raise_no_conditional_expression('__mod__')

    def __ne__(self, other):
        self.__raise_no_conditional_expression('__ne__')

    def __or__(self, other):
        self.__raise_no_conditional_expression('__or__')

    def __radd__(self, other):
        self.__raise_no_conditional_expression('__radd__')

    def __rand__(self, other):
        self.__raise_no_conditional_expression('__rand__')

    def __ror__(self, other):
        self.__raise_no_conditional_expression('__ror__')

    def __rmul__(self, other):
        self.__raise_no_conditional_expression('__rmul__')

    def __rxor__(self, other):
        self.__raise_no_conditional_expression('__rxor__')

    def __xor__(self, other):
        self.__raise_no_conditional_expression('__xor__')
