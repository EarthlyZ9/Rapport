import json
from django.test import Client
from http.cookies import SimpleCookie


class ClientRequest:
    def __init__(self, client: Client):
        self.client = client

    def __call__(
        self, type, url, data=None, cookies: dict = None, headers: dict = None
    ):
        content_type = "application/json"
        accept_header = "application/json"

        if headers is None:
            headers_dict = {}
        else:
            headers_dict = headers

        if cookies:
            self.client.cookies = SimpleCookie(cookies)

        if type == "get":
            res = self.client.get(
                url,
                {},
                content_type=content_type,
                HTTP_ACCEPT=accept_header,
                headers=headers_dict,
            )
        elif type == "post":
            res = self.client.post(
                url,
                json.dumps(data),
                content_type=content_type,
                HTTP_ACCEPT=accept_header,
                headers=headers_dict,
            )
        elif type == "del":
            res = self.client.delete(
                url,
                {},
                content_type=content_type,
                HTTP_ACCEPT=accept_header,
                headers=headers_dict,
            )
        elif type == "put":
            res = self.client.put(
                url,
                json.dumps(data),
                content_type=content_type,
                HTTP_ACCEPT=accept_header,
                headers=headers_dict,
            )
        else:
            res = self.client.patch(
                url,
                json.dumps(data),
                content_type=content_type,
                HTTP_ACCEPT=accept_header,
                headers=headers_dict,
            )
        return res

    def clear_cookies(self):
        self.client.cookies.clear()
