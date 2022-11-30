import allure
import pytest
from ui.base_ui import BaseUI


class TestsVKID(BaseUI):
    authorize = True

    @pytest.mark.vk_id
    def test_display_vk_id(self):
        username = self.user.username

        with allure.step('Проверяем, что VK_ID не отображается'):
            elem = self.main_page.find_located(self.main_page.locators.LOGIN_VK_ID)
            assert 'VK ID' not in elem.text

        with allure.step(f'Добавляем пользователю {username} VK ID'):
            vk_id = self.mock_client.post_vk_id(username)['vk_id']

        with allure.step('Проверяем, что он отображается после перезагрузки'):
            self.driver.refresh()
            elem = self.main_page.find_located(self.main_page.locators.LOGIN_VK_ID)
            assert f'VK ID: {vk_id}' in elem.text
zlib 