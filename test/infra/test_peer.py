#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import pytest
from time import sleep
import simplejson as json

sys.path.insert(
    0, path.dirname(path.dirname(path.dirname(path.abspath(__file__)))) + "/scripts",
)
from infra.rest import Rest
from domain.peer.model import PeerEvent, PeerStatus
from error import MyException
from ..helper import get_free_port


PKG = "skyway"


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # check path and header
        if (
            self.path
            == "/peers/my_id/events?token=pt-9749250e-d157-4f80-9ee2-359ce8524308"
        ):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            value = {
                "event": "OPEN",
                "params": {
                    "peer_id": "my_id",
                    "token": "pt-9749250e-d157-4f80-9ee2-359ce8524308",
                },
            }
            self.wfile.write(json.dumps(value))
        elif (
            self.path
            == "/peers/408/events?token=pt-9749250e-d157-4f80-9ee2-359ce8524308"
        ):
            self.send_response(408)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif (
            self.path
            == "/peers/my_id/status?token=pt-9749250e-d157-4f80-9ee2-359ce8524308"
        ):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            value = {"peer_id": "my_id", "disconnected": False}
            self.wfile.write(json.dumps(value))

    def do_POST(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/peers":
            # get request body
            content_length = int(self.headers["content-length"])
            body = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(body)
            if body["key"] == "valid_key":
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()

                data = {
                    u"command_type": u"PEERS_CREATE",
                    u"params": {
                        u"peer_id": body["peer_id"],
                        u"token": u"pt-9749250e-d157-4f80-9ee2-359ce8524308",
                    },
                }

                self.wfile.write("%s" % json.dumps(data))
            elif body["key"] == "invalid_json":
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write("{invalid: json")
            elif body["key"] == "invalid_key":
                self.send_response(403)
                self.send_header("Content-type", "application/json")
                self.end_headers()

    def do_DELETE(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/peers/my_id?token=pt-9749250e-d157-4f80-9ee2-359ce8524308":
            self.send_response(204)
            self.send_header("Content-type", "application/json")
            self.end_headers()


from infra.peer_api import PeerApi
from domain.peer.model import CreateRequestParams
from domain.common.model import PeerInfo


class TestPeerApi:
    def setup_method(self, method):
        port = get_free_port()
        self.url = "http://127.0.0.1:%s" % port
        self.rest = Rest(self.url)
        self.server = HTTPServer(("127.0.0.1", port), MyHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()
        self.peer_api = PeerApi(self.url)
        self.peer_info = PeerInfo("my_id", "pt-9749250e-d157-4f80-9ee2-359ce8524308")

        # for create_request tests
        self.create_request_json = {
            "key": "valid_key",
            "domain": "localhost",
            "peer_id": "my_id",
            "turn": True,
        }

    def teardown_method(self, method):
        self.server.shutdown()
        self.server_thread.join()
        del self.peer_info
        del self.peer_api
        del self.create_request_json
        del self.server_thread
        del self.server
        del self.rest
        del self.url

    def test_create_request_success(self):
        create_peer_params = CreateRequestParams(self.create_request_json)
        assert self.peer_api.create_request(create_peer_params) == PeerInfo(
            "my_id", "pt-9749250e-d157-4f80-9ee2-359ce8524308"
        )

    def test_create_request_json_parse_error(self):
        self.create_request_json["key"] = "invalid_json"
        self.create_peer_params = CreateRequestParams(self.create_request_json)
        with pytest.raises(MyException) as err:
            _result = self.peer_api.create_request(self.create_peer_params)
        assert err.value == MyException(
            "Expecting property name enclosed in double quotes"
        )

    def test_create_request_403(self):
        self.create_request_json["key"] = "invalid_key"
        self.create_peer_params = CreateRequestParams(self.create_request_json)
        with pytest.raises(MyException) as err:
            _result = self.peer_api.create_request(self.create_peer_params)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "peers"),
                "error": "403 Forbidden",
                "status": 403,
            }
        )

    def test_listen_event_success(self):
        assert self.peer_api.listen_event(self.peer_info) == PeerEvent(
            {
                "event": "OPEN",
                "params": {
                    "peer_id": self.peer_info.id(),
                    "token": self.peer_info.token(),
                },
            }
        )

    def test_listen_event_timeout(self):
        peer_info = PeerInfo("408", "pt-9749250e-d157-4f80-9ee2-359ce8524308")
        with pytest.raises(MyException) as err:
            _result = self.peer_api.listen_event(peer_info)

        assert err.value == MyException(
            {
                "url": "{}/{}".format(
                    self.url,
                    u"peers/408/events?token=pt-9749250e-d157-4f80-9ee2-359ce8524308",
                ),
                "error": "408 Request Timeout",
                "status": 408,
            }
        )

    def test_delete_request_success(self):
        assert self.peer_api.delete_request(self.peer_info)

    def test_status_request_success(self):
        assert self.peer_api.status_request(self.peer_info) == PeerStatus(
            "my_id", False
        )
