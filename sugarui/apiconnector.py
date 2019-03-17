# coding: utf-8
"""
API connector to the Sugar API core.
"""
import http
import urllib.parse
import requests
import sugarui.exceptions
from sugar.utils.objects import Singleton
# from twisted.internet.threads import deferToThread


class BaseCall:
    """
    Base network requests call.
    """
    def __init__(self, client):
        self._api_root_url = "https://localhost:8000"
        self.client = client

    def _request(self, uri, query=None, method="GET"):
        """
        Generic API request.

        :param uri:
        :return: JSON
        """
        verify_ssl = self.client._config.crypto.ssl.verify
        params = {}
        params.update(query or {})

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Accept": "application/json"
        }
        url = urllib.parse.urljoin(self._api_root_url, uri.lstrip("/"))
        response = requests.request(method, url, params=params, headers=headers, verify=verify_ssl)

        if response.status_code == http.HTTPStatus.UNAUTHORIZED:
            raise sugarui.exceptions.UnauthorisedError("{} for {}".format(response.text, url))
        elif response.status_code != http.HTTPStatus.OK:
            raise sugarui.exceptions.UnknownResourceError("{} at {}".format(response.text, url))

        try:
            obj = response.json()
        except Exception as ex:
            raise Exception(ex)

        return obj


class Systems(BaseCall):
    """
    Systems connector.
    """
    class System:
        def __init__(self, data):
            self.data = data

        def __str__(self):
            return self.data["host"]

    def get_status(self, id=None) -> list:
        """
        Get client status.

        :param id:
        :return: list of systems
        """
        out = []
        for system in self._request("/clients/status")["systems"].values():
            if (id is not None and system["id"] == id) or id is None:
                out.append(Systems.System(system))

        return out


@Singleton
class SugarAPIClient:
    """
    Sugar API composite client.
    """
    def __init__(self, config):
        self._config = config
        self.systems = Systems(self)
