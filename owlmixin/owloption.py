# coding: utf-8

from typing import Generic, TypeVar

T = TypeVar('T')


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

    def is_none(self):
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

    def __repr__(self):
        return f'Option --> {self.get()}'
