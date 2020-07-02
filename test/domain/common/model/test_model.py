# -*- coding: utf-8 -*-
import pytest
import sys
from os import path

sys.path.insert(
    0,
    path.dirname(
        path.dirname(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))))
    )
    + "/scripts",
)
from error import MyException
from domain.common.model import PeerInfo


class TestPeerInfo:
    def setup_method(self, method):
        self.json = {
            "key": "key",
            "domain": "localhost",
            "peer_id": "my_id",
            "turn": True,
        }

    def teardown_method(self, method):
        del self.json

    @pytest.mark.parametrize(
        "peer_id, token",
        [
            (u"my_id", u"pt-102127d9-30de-413b-93f7-41a33e39d82b"),
            ("my_id", "pt-102127d9-30de-413b-93f7-41a33e39d82b"),
        ],
    )
    def test_create_success(self, peer_id, token):
        peer_info = PeerInfo(peer_id, token)
        assert peer_info.id() == u"my_id", "peer_id is not correct"
        assert (
            peer_info.token() == u"pt-102127d9-30de-413b-93f7-41a33e39d82b"
        ), "token is not correct"

    @pytest.mark.parametrize(
        "peer_id, token",
        [
            (0, u"pt-102127d9-30de-413b-93f7-41a33e39d82b"),
            (u"peer_id", 0),
            (u"", u"pt-102127d9-30de-413b-93f7-41a33e39d82b"),
            (u"token_len_0", u""),
            (u"short_token", u"pt-102127d9-30de-413b-93f7-41a33e39d82"),
            (u"long_token", u"pt-102127d9-30de-413b-93f7-41a33e39d82b3"),
        ],
    )
    def test_create_peer_info_failed(self, peer_id, token):
        with pytest.raises(MyException):
            _peer_info = PeerInfo(peer_id, token)
