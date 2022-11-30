from api.client import Client

class ApiClient(Client):
    def __init__(self, base_url):
        super().__init__(base_url)

    def post_login(self, username, password):
        location = '/login'

        payload = {
            "username": username,
            "password": password,
            "submit": "Login"
        }

        resp = self._request(method='POST',
                             location=location,
                             json=payload,
                             # expected_status=200
                             )
        return resp

    def post_ui_reg(self, data):
        location = '/reg'
        payload = data
        resp = self._request(method='POST',
                             location=location,
                             data=payload)
        return resp

    def post_api_reg(self, data, exp_status):
        location = '/api/user'
        payload = data
        resp = self._request(method='POST',
                             location=location,
                             json=payload,
                             expected_status=exp_status,
                             jsonify=True)
        return resp

    def delete_user(self, username, exp_status=204):
        location = f'/api/user/{username}'
        resp = self._request(method='DELETE',
                             location=location,
                             expected_status=exp_status,
                             # jsonify=True
                             )
        return resp

    def change_pass(self, username, password):
        location = f'/api/user/{username}/change-password'

        payload = {
            'password': password
        }

        resp = self._request(method='PUT',
                             location=location,
                             json=payload,
                             # expected_status=200
                             )
        return resp

    def block_user(self, username):
        location = f'api/user/{username}/block'

        resp = self._request(method='POST',
                             location=location,
                             # expected_status=200,
                             jsonify=True
                             )
        return resp

    def unblock_user(self, username):
        location = f'api/user/{username}/accept'

        resp = self._request(method='POST',
                             location=location,
                             # expected_status=200,
                             jsonify=True
                             )
        return resp

    def check_status(self):
        location = f'status'

        resp = self._request(method='GET',
                             location=location,
                             expected_status=200,
                             jsonify=True
                             )
        return resp
