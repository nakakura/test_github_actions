# -*- coding: utf-8 -*-
# This module defines the user's error type


class MyException(Exception):
    def __init__(self, value=None):
        # type (dict) -> None
        if value is None:
            self.__value = {}
        else:
            self.__value = value

    def message(self):
        # type () -> dict
        return self.__value

    def __eq__(self, other):
        if not isinstance(other, MyException):
            return NotImplemented
        return self.__value == other.__value

    def __lt__(self, other):
        if not isinstance(other, MyException):
            return NotImplemented
        return self.__value < other.__value

    def __ne__(self, other):
        return not self.__eq__(other)
