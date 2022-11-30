import os

import pytest
from selenium import webdriver

import settings
from ui.pages.main_page import MainPage
from ui.pages.reg_page import RegPage
from ui.pages.login_page import LoginPage

from api.client_api import ApiClient
from api.client_mock import MockClient
from mysql.mysql_client import MysqlClient
from builder.builder import Builder

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope='session')
def base_url():
    return f'http://{settings.APP_NAME}:{settings.APP_PORT}/'


@pytest.fixture(scope='session')
def mock_url():
    return f'http://{settings.MOCK_HOST}:{settings.MOCK_PORT}/'


@pytest.fixture(scope='session')
def driver():
    firefox_options = webdriver.FirefoxOptions()
    driver = webdriver.Remote(command_executor=f'http://{settings.SELENOID_NAME}:{settings.SELENOID_PORT}/wd/hub',
                              options=firefox_options)
    # driver = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope='session')
def api_client(base_url):
    api_client = ApiClient(base_url)
    api_client.post_login(settings.USER_NAME, settings.USER_PASSWORD)
    return api_client


@pytest.fixture(scope='session')
def mock_client(mock_url):
    mock_client = MockClient(mock_url)
    return mock_client


@pytest.fixture(scope='session')
def mysql_client():
    username = settings.USER_NAME

    mysql_client = MysqlClient(host=settings.MYSQL_NAME,
                               port=settings.MYSQL_PORT,
                               db_name=settings.MYSQL_DATABASE,
                               user='root',
                               password=settings.MYSQL_ROOT_PASSWORD)
    mysql_client.connect(db_created=True)

    try:
        mysql_client.insert_user(username, username, username, username, settings.USER_PASSWORD, username + '@y.y')
    except Exception:
        mysql_client.session.rollback()

    yield mysql_client

    mysql_client.delete_user(username)
    mysql_client.connection.close()


@pytest.fixture(scope='session')
def builder():
    builder = Builder()
    return builder


@pytest.fixture(scope='session')
def repo_root():
    return os.path.abspath(os.path.join(__file__, os.path.pardir))


@pytest.fixture()
def login_page(driver):
    return LoginPage(driver=driver)


@pytest.fixture()
def reg_page(driver):
    return RegPage(driver=driver)


@pytest.fixture()
def main_page(driver):
    return MainPage(driver=driver)


@pytest.fixture()
def create_test_user():
    def _create(mysql_client, username, user_data):
        global user, mysql
        mysql, user = mysql_client, username
        mysql.insert_user(*user_data)
    yield _create
    mysql.delete_user(user)
