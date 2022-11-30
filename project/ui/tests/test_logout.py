import allure
import pytest
from ui.base_ui import BaseUI


class TestsMainPage(BaseUI):
    authorize = True

    @pytest.mark.ui_login
    def test_logout(self):
        username = self.user.username
        with allure.step('Нажимаем на кнопку Logout'):
            self.main_page.logout()

        with allure.step('Проверяем, появилась ли кнпока LOGIN'):
            assert self.main_page.find_located(self.login_page.locators.LOGIN_BUTTON)

        with allure.step(f'Проверяем в бд active у пользователя {username}'):
            assert self.mysql_client.select_user(username).active == 0
