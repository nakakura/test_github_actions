# -*- coding: utf-8 -*-
import sys
from os import path

sys.path.insert(
    0, path.dirname(path.dirname(path.abspath(__file__))) + "/scripts",
)
from error import MyException


class TestMyError:
    def setup_method(self, method):
        self.exception = MyException({"data": "value"})

    def teardown_method(self, method):
        del self.exception

    def test_check_value(self):
        assert self.exception.message() == {"data": "value"}

    def test_eq(self):
        assert self.exception == MyException({"data": "value"})

    def test_ne(self):
        assert self.exception != MyException({"data": "value2"})
