import pytest


class ApiBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client, api_client, builder, create_test_user):
        self.mysql_client = mysql_client
        self.api_client = api_client
        self.builder = builder

        self.user, self.user_data = self.builder.user(type='db')
        create_test_user(self.mysql_client, self.user.username, self.user_data)

    @pytest.fixture()
    def create_user(self):
        def _create(username, user_data, exp_status=None):
            global user
            user = username
            resp = self.api_client.post_api_reg(user_data, exp_status)
            return resp
        yield _create
        self.mysql_client.delete_user(user)
