#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
import sys
from os import path
import dependency_injector.providers as providers


sys.path.insert(
    0, path.dirname(path.dirname(path.dirname(path.abspath(__file__)))) + "/scripts",
)


PKG = "skyway"


from abc import ABCMeta, abstractmethod


class Factory:
    __domain = 10  # "htttp://localhost:8000"

    @classmethod
    def set_domain(cls, domain):
        cls.__domain = domain

    @classmethod
    def create_peer_api(cls):
        factory = providers.Factory(Caller, param=1, call=Concrete(cls.__domain))
        return factory()


class Interface:
    __metaclass__ = ABCMeta

    @abstractmethod
    def create_request(self, num):
        # type: (int) -> None
        pass


class Concrete(Interface):
    def __init__(self, param):
        self.param = param

    def create_request(self, num):
        # type: (int) -> None
        print num + self.param
        pass


class Caller:
    def __init__(self, param, call):
        self.param = param
        self.call = call
        pass

    def add(self, val):
        self.call.create_request(self.param + val)


class TestPeerApi:
    def setup_method(self, method):
        Factory.set_domain(100)
        pass

    def teardown_method(self, method):
        pass

    def test_inject(self):
        instance = Factory.create_peer_api()
        instance.add(10)
