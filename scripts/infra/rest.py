#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from error import MyException


class Rest:
    def __init__(self, domain):
        # type (str) -> None
        self.__domain = domain
        pass

    @staticmethod
    def __parse_response(resp, expected_code):
        # type: (requests.Response, int) -> dict
        if resp.status_code == expected_code and expected_code == 204:
            return {}
        elif resp.status_code == expected_code:
            return resp.json()
        elif resp.status_code == 400:
            raise MyException(
                {"url": resp.url, "error": "400 Bad Request", "status": 400}
            )
        elif resp.status_code == 403:
            raise MyException(
                {"url": resp.url, "error": "403 Forbidden", "status": 403}
            )
        elif resp.status_code == 404:
            raise MyException(
                {"url": resp.url, "error": "404 Not Found", "status": 404}
            )
        elif resp.status_code == 405:
            raise MyException(
                {"url": resp.url, "error": "405 Method Not Allowed", "status": 405}
            )
        elif resp.status_code == 406:
            raise MyException(
                {"url": resp.url, "error": "406 Not Acceptable", "status": 406}
            )
        elif resp.status_code == 408:
            raise MyException(
                {"url": resp.url, "error": "408 Request Timeout", "status": 408}
            )
        else:
            raise MyException(
                {
                    "url": resp.url,
                    "error": "Unexpected Status Code",
                    "status": resp.status_code,
                }
            )

    def get(self, path, expected_code, connect_timeout=1.0, read_timeout=30.0):
        # type: (str, int, float, float) -> dict
        headers = {"Content-Type": "application/json"}
        # SkyWay WebRTC Gateway's longpoll methods return timeout every 30secs.
        url = "{}/{}".format(self.__domain, path)
        try:
            resp = requests.get(
                url, headers=headers, timeout=(connect_timeout, read_timeout),
            )
        except requests.ConnectionError:
            raise MyException(
                {"url": url, "error": "Server Disconnected",}
            )

        return Rest.__parse_response(resp, expected_code)

    def post(self, path, payload, expected_code, connect_timeout=1.0, read_timeout=1.0):
        # type: (str, dict, int, float, float) -> dict
        headers = {"Content-Type": "application/json"}
        url = "{}/{}".format(self.__domain, path)
        try:
            resp = requests.post(
                "{}/{}".format(self.__domain, path),
                headers=headers,
                json=payload,
                timeout=(connect_timeout, read_timeout),
            )
        except requests.ConnectionError:
            raise MyException(
                {"url": url, "error": "Server Disconnected",}
            )

        return Rest.__parse_response(resp, expected_code)

    def put(self, path, payload, expected_code, connect_timeout=1.0, read_timeout=1.0):
        # type: (str, dict, int, float, float) -> dict
        headers = {"Content-Type": "application/json"}
        url = "{}/{}".format(self.__domain, path)
        try:
            resp = requests.put(
                "{}/{}".format(self.__domain, path),
                headers=headers,
                json=payload,
                timeout=(connect_timeout, read_timeout),
            )
        except requests.ConnectionError:
            raise MyException(
                {"url": url, "error": "Server Disconnected",}
            )

        return Rest.__parse_response(resp, expected_code)

    def delete(self, path, expected_code, connect_timeout=1.0, read_timeout=1.0):
        # type: (str, int, float, float) -> dict
        headers = {"Content-Type": "application/json"}
        url = "{}/{}".format(self.__domain, path)
        try:
            resp = requests.delete(
                "{}/{}".format(self.__domain, path),
                headers=headers,
                timeout=(connect_timeout, read_timeout),
            )
        except requests.ConnectionError:
            raise MyException(
                {"url": url, "error": "Server Disconnected",}
            )

        return Rest.__parse_response(resp, expected_code)
