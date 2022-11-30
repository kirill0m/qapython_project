import pytest
from _pytest.fixtures import FixtureRequest
from builder.builder import Builder
from ui.pages.login_page import LoginPage
from ui.pages.main_page import MainPage
from ui.pages.reg_page import RegPage
from ui.pages.base_page import BasePage


class BaseUI:
    authorize = False

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, driver, base_url, mysql_client, mock_client, create_test_user, builder, request: FixtureRequest):
        self.driver = driver
        self.mock_client = mock_client
        self.builder = builder
        self.mysql_client = mysql_client

        BasePage.base_url = base_url

        self.login_page: LoginPage = (request.getfixturevalue('login_page'))
        self.reg_page: RegPage = (request.getfixturevalue('reg_page'))
        self.main_page: MainPage = (request.getfixturevalue('main_page'))

        self.user, self.user_data = self.builder.user(type='db')
        create_test_user(self.mysql_client, self.user.username, self.user_data)

        if self.authorize:
            self.login_page.login(self.user.username, self.user.password)

    def check_min_max_attrs(self, name, field):
        try:
            min = int(field.get_attribute('minlength'))
            max = int(field.get_attribute('maxlength'))
            return min, max
        except TypeError:
            pytest.fail(f'У поля {name} нет атрибута минимальной/максимальной длины')

    @pytest.fixture()
    def create_user(self):
        def _create(username, user_data):
            global user
            user = username
            self.reg_page.fill_user_form(user_data)
            self.reg_page.submit_and_create()
        yield _create
        self.mysql_client.delete_user(user)
