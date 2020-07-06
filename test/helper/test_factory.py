#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import simplejson as json

sys.path.insert(
    0, path.dirname(path.dirname(path.dirname(path.abspath(__file__)))) + "/scripts",
)
from helper.factory import Factory
from ..helper_module import get_free_port
from application.peer.create_request import CreateRequest
from domain.common.model import PeerInfo

PKG = "skyway"


class MyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/peers":
            # get request body
            content_length = int(self.headers["content-length"])
            body = self.rfile.read(content_length).decode("utf-8")
            body = json.loads(body)
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


class TestFactory:
    def setup_method(self, method):
        port = get_free_port()
        self.url = "http://127.0.0.1:%s" % port
        self.server = HTTPServer(("127.0.0.1", port), MyHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

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
        del self.create_request_json
        del self.server_thread
        del self.server
        del self.url

    def test_feed_peer_api(self):
        Factory.set_domain(self.url)
        create_request = Factory.feed_peer_api(CreateRequest)
        assert create_request.run(
            {
                "key": "KEY_FOO",
                "domain": "example.com",
                "peer_id": "ID_FOO",
                "turn": True,
            }
        ) == PeerInfo("ID_FOO", "pt-9749250e-d157-4f80-9ee2-359ce8524308")
