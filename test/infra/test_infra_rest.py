#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from os import path
import BaseHTTPServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import threading
import pytest
from time import sleep

sys.path.insert(
    0, path.dirname(path.dirname(path.dirname(path.abspath(__file__)))) + "/scripts",
)
from infra.rest import Rest
from error import MyException
from ..helper_module import get_free_port


PKG = "skyway"


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/success":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write('{"hoge": "moge"}')
        elif self.path == "/disconnect":
            return
        elif self.path == "/400":
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/403":
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/404":
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/405":
            self.send_response(405)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/406":
            self.send_response(406)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/408":
            self.send_response(408)
            self.send_header("Content-type", "application/json")
            self.end_headers()

    def do_POST(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/success":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # echo back request body
            content_length = int(self.headers["content-length"])
            data = self.rfile.read(content_length).decode("utf-8")
            self.wfile.write("%s" % data)
        elif self.path == "/disconnect":
            return
        elif self.path == "/400":
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/403":
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/404":
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/405":
            self.send_response(405)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/406":
            self.send_response(406)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/408":
            self.send_response(408)
            self.send_header("Content-type", "application/json")
            self.end_headers()

    def do_PUT(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/success":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()

            # echo back request body
            content_length = int(self.headers["content-length"])
            data = self.rfile.read(content_length).decode("utf-8")
            self.wfile.write("%s" % data)
        elif self.path == "/disconnect":
            return
        elif self.path == "/400":
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/403":
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/404":
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/405":
            self.send_response(405)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/406":
            self.send_response(406)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/408":
            self.send_response(408)
            self.send_header("Content-type", "application/json")
            self.end_headers()

    def do_DELETE(self):
        # check path and header
        assert self.headers.get("Content-Type") == "application/json"

        if self.path == "/success":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write('{"hoge": "moge"}')
        elif self.path == "/disconnect":
            return
        elif self.path == "/400":
            self.send_response(400)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/403":
            self.send_response(403)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/404":
            self.send_response(404)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/405":
            self.send_response(405)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/406":
            self.send_response(406)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        elif self.path == "/408":
            self.send_response(408)
            self.send_header("Content-type", "application/json")
            self.end_headers()


class TestRest:
    def setup_method(self, method):
        port = get_free_port()
        self.url = "http://127.0.0.1:%s" % port
        self.rest = Rest(self.url)
        self.server = HTTPServer(("127.0.0.1", port), MyHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.start()

    def teardown_method(self, method):
        self.server.shutdown()
        self.server_thread.join()
        del self.server_thread
        del self.server
        del self.rest
        del self.url

    def test_get_success(self):
        result = self.rest.get("success", 200)
        assert result == {"hoge": "moge"}

    def test_get_invalid_code(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("success", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "success"),
                "error": "Unexpected Status Code",
                "status": 200,
            }
        )

    def test_get_400(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("400", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "400"),
                "error": "400 Bad Request",
                "status": 400,
            }
        )

    def test_get_403(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("403", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "403"),
                "error": "403 Forbidden",
                "status": 403,
            }
        )

    def test_get_404(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("404", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "404"),
                "error": "404 Not Found",
                "status": 404,
            }
        )

    def test_get_405(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("405", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "405"),
                "error": "405 Method Not Allowed",
                "status": 405,
            }
        )

    def test_get_406(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("406", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "406"),
                "error": "406 Not Acceptable",
                "status": 406,
            }
        )

    def test_get_408(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("408", 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "408"),
                "error": "408 Request Timeout",
                "status": 408,
            }
        )

    def test_get_disconnect(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.get("disconnect", 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "disconnect"),
                "error": "Server Disconnected",
            }
        )

    def test_post_success(self):
        result = self.rest.post("success", {"data": "hoge"}, 200)
        assert result == {"data": "hoge"}

    def test_post_400(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("400", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "400"),
                "error": "400 Bad Request",
                "status": 400,
            }
        )

    def test_post_403(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("403", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "403"),
                "error": "403 Forbidden",
                "status": 403,
            }
        )

    def test_post_404(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("404", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "404"),
                "error": "404 Not Found",
                "status": 404,
            }
        )

    def test_post_405(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("405", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "405"),
                "error": "405 Method Not Allowed",
                "status": 405,
            }
        )

    def test_post_406(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("406", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "406"),
                "error": "406 Not Acceptable",
                "status": 406,
            }
        )

    def test_post_408(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("408", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "408"),
                "error": "408 Request Timeout",
                "status": 408,
            }
        )

    def test_post_disconnect(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.post("disconnect", {"data": "hoge"}, 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "disconnect"),
                "error": "Server Disconnected",
            }
        )

    def test_put_success(self):
        result = self.rest.put("success", {"data": "hoge"}, 200)
        assert result == {"data": "hoge"}

    def test_put_400(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("400", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "400"),
                "error": "400 Bad Request",
                "status": 400,
            }
        )

    def test_put_403(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("403", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "403"),
                "error": "403 Forbidden",
                "status": 403,
            }
        )

    def test_put_404(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("404", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "404"),
                "error": "404 Not Found",
                "status": 404,
            }
        )

    def test_put_405(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("405", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "405"),
                "error": "405 Method Not Allowed",
                "status": 405,
            }
        )

    def test_put_406(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("406", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "406"),
                "error": "406 Not Acceptable",
                "status": 406,
            }
        )

    def test_put_408(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("408", {}, 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "408"),
                "error": "408 Request Timeout",
                "status": 408,
            }
        )

    def test_put_disconnect(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.put("disconnect", {"data": "hoge"}, 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "disconnect"),
                "error": "Server Disconnected",
            }
        )

    def test_delete_success(self):
        result = self.rest.delete("success", 200)
        assert result == {"hoge": "moge"}

    def test_delete_400(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("400", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "400"),
                "error": "400 Bad Request",
                "status": 400,
            }
        )

    def test_delete_403(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("403", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "403"),
                "error": "403 Forbidden",
                "status": 403,
            }
        )

    def test_delete_404(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("404", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "404"),
                "error": "404 Not Found",
                "status": 404,
            }
        )

    def test_delete_405(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("405", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "405"),
                "error": "405 Method Not Allowed",
                "status": 405,
            }
        )

    def test_delete_406(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("406", 201)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "406"),
                "error": "406 Not Acceptable",
                "status": 406,
            }
        )

    def test_delete_408(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("408", 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "408"),
                "error": "408 Request Timeout",
                "status": 408,
            }
        )

    def test_delete_disconnect(self):
        with pytest.raises(MyException) as err:
            _result = self.rest.delete("disconnect", 200)
        assert err.value == MyException(
            {
                "url": "{}/{}".format(self.url, "disconnect"),
                "error": "Server Disconnected",
            }
        )
