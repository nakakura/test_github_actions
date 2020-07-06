# -*- coding: utf-8 -*-
import simplejson as json

from domain.common.model import PeerInfo
from domain.peer.model import CreateRequestParams, PeerEvent, PeerStatus
from rest import Rest
from error import MyException


class PeerApi:
    def __init__(self, domain):
        # type: (str) -> None
        self.__rest = Rest(domain)

    def create_request(self, param):
        """
        Send a PeerObject create request
        http://35.200.46.204/#/1.peers/peer

        :param CreateRequestParams params: Parameters for creating a PeerObject
        :return: Information to identify the object
        :rtype: PeerInfo
        """
        try:
            response = self.__rest.post("peers", param.json(), 201)
        except json.JSONDecodeError as e:
            raise MyException(e.msg)

        return PeerInfo(response["params"]["peer_id"], response["params"]["token"])

    def listen_event(self, peer_info):
        """
        Get an event of PeerObject
        http://35.200.46.204/#/1.peers/peer_event

        :param PeerInfo peer_info: Indicates which peer object to subscribe events
        :return: An event from PeerObject
        :rtype: PeerEvent
        """
        try:
            response = self.__rest.get(
                "peers/{}/events?token={}".format(peer_info.id(), peer_info.token()),
                200,
            )
        except json.JSONDecodeError as e:
            raise MyException(e.msg)

        return PeerEvent(response)

    def delete_request(self, peer_info):
        """
        Send a Delete Request of PeerObject
        Accessing DELETE /peers API Internally
        http://35.200.46.204/#/1.peers/peer_destroy

        :param PeerInfo peer_info: Indicates which peer object to be deleted
        :return: Delete succeed or not
        :rtype: bool
        """
        try:
            self.__rest.delete(
                "peers/{}?token={}".format(peer_info.id(), peer_info.token()), 204
            )
        except json.JSONDecodeError as e:
            raise MyException(e.msg)

        return True

    def status_request(self, peer_info):
        """
        Request status of Peer Object
        Accessing GET /peers/{peer_id}/status API Internally
        http://35.200.46.204/#/1.peers/peer_status

        :param PeerInfo peer_info: Indicates which peer object to be deleted
        :return: Status of the PeerObject
        :rtype: PeerStatus
        """
        json = self.__rest.get(
            "peers/{}/status?token={}".format(peer_info.id(), peer_info.token()), 200
        )
        return PeerStatus(json["peer_id"], json["disconnected"])
