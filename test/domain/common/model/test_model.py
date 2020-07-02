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
from domain.common.model import (
    PeerInfo,
    DataId,
    DataConnectionId,
    MediaId,
    RtcpId,
    MediaConnectionId,
)


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


# ----------Data ----------
class TestDataId:
    def setup_method(self, method):
        self.data_id = DataId(u"da-50a32bab-b3d9-4913-8e20-f79c90a6a211")

    def teardown_method(self, method):
        del self.data_id

    def test_compare_same_id(self):
        assert self.data_id == DataId("da-50a32bab-b3d9-4913-8e20-f79c90a6a211")

    def test_compare_different_id(self):
        assert self.data_id != DataId(u"da-14a32bab-b3d9-4913-8e20-f79c90a6a211")

    @pytest.mark.parametrize(
        "data_id",
        [
            # short
            u"da-50a32bab-b3d9-4913-8e20-f79c90a6a21",
            # long
            u"da-50a32bab-b3d9-4913-8e20-f79c90a6a2112",
            # wrong prefix
            u"dc-50a32bab-b3d9-4913-8e20-f79c90a6a211",
        ],
    )
    def test_create_fail(self, data_id):
        with pytest.raises(MyException):
            _data_id = DataId(data_id)


class TestDataConnectionId:
    def setup_method(self, method):
        self.data_connection_id = DataConnectionId(
            u"dc-50a32bab-b3d9-4913-8e20-f79c90a6a211"
        )

    def teardown_method(self, method):
        del self.data_connection_id

    def test_compare_same_id(self):
        assert self.data_connection_id == DataConnectionId(
            "dc-50a32bab-b3d9-4913-8e20-f79c90a6a211"
        )

    def test_compare_different_id(self):
        assert self.data_connection_id != DataConnectionId(
            u"dc-10032bab-b3d9-4913-8e20-f79c90a6a211"
        )

    @pytest.mark.parametrize(
        "data_connection_id",
        [
            # short
            u"dc-50a32bab-b3d9-4913-8e20-f79c90a6a21",
            # long
            u"dc-50a32bab-b3d9-4913-8e20-f79c90a6a2112",
            # wrong prefix
            u"da-50a32bab-b3d9-4913-8e20-f79c90a6a211",
        ],
    )
    def test_create_fail(self, data_connection_id):
        with pytest.raises(MyException):
            _data_connection_id = DataConnectionId(data_connection_id)


# ----------Media ----------
class TestMediaId:
    def setup_method(self, method):
        self.media_id = MediaId(u"vi-50a32bab-b3d9-4913-8e20-f79c90a6a211")

    def teardown_method(self, method):
        del self.media_id

    def test_compare_same_id(self):
        assert self.media_id == MediaId("vi-50a32bab-b3d9-4913-8e20-f79c90a6a211")

    def test_compare_different_id(self):
        assert self.media_id != MediaId(u"au-14a32bab-b3d9-4913-8e20-f79c90a6a211")

    @pytest.mark.parametrize(
        "media_id",
        [
            # short
            u"vi-50a32bab-b3d9-4913-8e20-f79c90a6a21",
            # long
            u"au-50a32bab-b3d9-4913-8e20-f79c90a6a2112",
            # wrong prefix
            u"dc-50a32bab-b3d9-4913-8e20-f79c90a6a211",
        ],
    )
    def test_create_fail(self, media_id):
        with pytest.raises(MyException):
            _media_id = MediaId(media_id)


class TestRtcpId:
    def setup_method(self, method):
        self.rtcp_id = RtcpId(u"rc-970f2e5d-4da0-43e7-92b6-796678c104ad")

    def teardown_method(self, method):
        del self.rtcp_id

    def test_compare_same_id(self):
        assert self.rtcp_id == RtcpId("rc-970f2e5d-4da0-43e7-92b6-796678c104ad")

    def test_compare_different_id(self):
        assert self.rtcp_id != RtcpId(u"rc-14a32bab-b3d9-4913-8e20-f79c90a6a211")

    @pytest.mark.parametrize(
        "rtcp_id",
        [
            # short
            u"rc-50a32bab-b3d9-4913-8e20-f79c90a6a21",
            # long
            u"rc-50a32bab-b3d9-4913-8e20-f79c90a6a2112",
            # wrong prefix
            u"pt-50a32bab-b3d9-4913-8e20-f79c90a6a211",
        ],
    )
    def test_create_fail(self, rtcp_id):
        with pytest.raises(MyException):
            _media_id = MediaId(rtcp_id)


class TestMediaConnectionId:
    def setup_method(self, method):
        self.media_connection_id = MediaConnectionId(
            u"mc-102127d9-30de-413b-93f7-41a33e39d82b"
        )

    def teardown_method(self, method):
        del self.media_connection_id

    def test_compare_same_id(self):
        assert self.media_connection_id == MediaConnectionId(
            "mc-102127d9-30de-413b-93f7-41a33e39d82b"
        )

    def test_compare_different_id(self):
        assert self.media_connection_id != MediaConnectionId(
            u"mc-aa2127d9-30de-413b-93f7-41a33e39d82b"
        )

    @pytest.mark.parametrize(
        "media_id",
        [
            # short
            u"mc-50a32bab-b3d9-4913-8e20-f79c90a6a21",
            # long
            u"mc-50a32bab-b3d9-4913-8e20-f79c90a6a2112",
            # wrong prefix
            u"pt-50a32bab-b3d9-4913-8e20-f79c90a6a211",
        ],
    )
    def test_create_fail(self, media_id):
        with pytest.raises(MyException):
            _media_id = MediaId(media_id)
