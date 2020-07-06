#!/usr/bin/env python
# -*- coding: utf-8 -*-
from os import path
import dependency_injector.providers as providers
from abc import ABCMeta, abstractmethod

from infra.peer_api import PeerApi


class Factory:
    __domain = "htttp://localhost:8000"

    @classmethod
    def set_domain(cls, domain):
        cls.__domain = domain

    @classmethod
    def feed_peer_api(cls, CLASS):
        factory = providers.Factory(CLASS, peer_api=PeerApi(cls.__domain))
        return factory()
