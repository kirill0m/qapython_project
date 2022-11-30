import requests
from urllib.parse import urljoin


class InternalServerError(Exception):
    pass


class ResponseStatusCodeException(Exception):
    pass


class Client():
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()

    def _request(self, method,
                 location=None,
                 headers=None,
                 data=None,
                 json=None,
                 expected_status=None,
                 jsonify=False,
                 params=None):
        url = self.base_url if location is None else urljoin(self.base_url, location)

        response = self.session.request(method=method, url=url, headers=headers, data=data, json=json,
                                        params=params, allow_redirects=True)

        if str(response.status_code).startswith('5'):
            raise InternalServerError

        if expected_status is not None and response.status_code != expected_status:
            raise ResponseStatusCodeException

        if jsonify:
            return response.json()

        return response
