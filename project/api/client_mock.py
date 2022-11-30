from api.client import Client


class MockClient(Client):
    def __init__(self, base_url):
        super().__init__(base_url)

    def post_vk_id(self, username):
        location = f'vk_id/{username}'
        resp = self._request(method='POST',
                             location=location,
                             expected_status=201,
                             jsonify=True)
        return resp
