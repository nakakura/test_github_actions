# -*- coding: utf-8 -*-
from error import MyException


class PeerInfo:
    """
    Information for identifying PeerObject
    Fields
    peer_id: String, not null, an ID of Peer Object
    token: String, not null, UUID
    """

    def __init__(self, peer_id, token):
        # type: (unicode, unicode) -> None
        if isinstance(peer_id, str):
            peer_id = peer_id.decode("utf-8")
        if not isinstance(peer_id, unicode) or len(peer_id) == 0:
            raise MyException("peer_id: invalid parameter in PeerInfo")
        self.__peer_id = peer_id

        if isinstance(token, str):
            token = token.decode("utf-8")
        # TOKEN is prefix(pt-, 3words) + UUID(36words) = 39words
        if (
            not isinstance(token, unicode)
            or len(token) != 39
            or not token.startswith("pt-")
        ):
            raise MyException("token: invalid parameter in PeerInfo")
        self.__token = token

    def id(self):
        # type: () -> unicode
        return self.__peer_id

    def token(self):
        # type: () -> unicode
        return self.__token

    def json(self):
        # type: () -> dict
        return {u"peer_id": self.__peer_id, u"token": self.__token}

    def __eq__(self, other):
        if not isinstance(other, PeerInfo):
            return NotImplemented
        return self.__peer_id == other.__peer_id and self.__token == other.__token

    def __ne__(self, other):
        return not self.__eq__(other)
