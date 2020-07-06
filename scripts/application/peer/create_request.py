# -*- coding: utf-8 -*-
from domain.peer.interface import IPeerApi
from domain.peer.model import CreateRequestParams, PeerInfo
from error import MyException


class CreateRequest:
    def __init__(self, peer_api):
        # type: (IPeerApi) -> None
        if not isinstance(peer_api, IPeerApi):
            raise MyException("CreateRequest needs IPeerApi")
        self.__api = peer_api

    def run(self, json):
        # type: (dict) -> PeerInfo
        params = CreateRequestParams(json)
        return self.__api.create_request(params)
