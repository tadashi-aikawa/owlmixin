# coding: utf-8

from typing import Generic, TypeVar


T = TypeVar('T')


class Option(Generic[T]):
    def __init__(self, value):
        self.value = value

    def get(self) -> T:
        return self.value

    def is_none(self):
        return self.value is None
