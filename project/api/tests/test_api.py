import pytest
import allure
from api.base_api import ApiBase


class TestsCreateUser(ApiBase):
    @pytest.mark.valid
    def test_create_user_positive(self, create_user):
        user, user_json = self.builder.user(type='api')

        with allure.step(f'Создаем пользователя {user.username}, проверям статус код'):
            resp = create_user(user.username, user_json, exp_status=210)

        with allure.step(f'Проверяем статус в ответе'):
            assert resp['status'] == 'success'

        with allure.step(f'Проверяем, появился ли {user.username} в базе данных'):
            assert self.mysql_client.select_user(user.username)

    @pytest.mark.create_negative
    @pytest.mark.parametrize(
        'field_length',
        [
            *[{'username': length} for length in [0, 17]],
            *[{'password': length} for length in [0, 5, 21]],
            *[{'email': length} for length in [0, 5, 65]]
        ]
    )
    def test_create_user_negative(self, field_length, create_user):
        name = next(iter(field_length))
        length = next(iter(field_length.values()))

        value = self.builder.generate_value(length)

        user, user_json = self.builder.user(**{name: value})

        with allure.step(f'Создаем пользователя {user.username} с {field_length}, проверям статус код'):
            resp = create_user(user.username, user_json)

            status = resp['status']

            if status == 'success':
                pytest.fail(f"Пользователь зарегистрирован с '{value}' в {name}")

        with allure.step(f'Проверяем статус в ответе'):
            assert status == 'failed'


class TestsDeleteUser(ApiBase):

    @pytest.mark.API
    def test_delete_existing_user(self):
        username = self.user.username

        with allure.step(f'Удаляем пользователя {username}, проверям статус код'):
            self.api_client.delete_user(username)

        with allure.step(f'Проверяем, нет ли записей в бд по {username}'):
            assert self.mysql_client.select_user(username) is None


class TestsModifyUser(ApiBase):
    @pytest.mark.API
    def test_change_pass(self):
        username = self.user.username
        new_pass = self.builder.generate_value(7)

        with allure.step(f'Меняем пароль у пользователя {username}, проверяем статус код'):
            self.api_client.change_pass(username, new_pass)

        with allure.step(f'Проверяем, изменился ли пароль в бд'):
            assert new_pass == self.mysql_client.select_user(username).password


    @pytest.mark.API
    def test_block_user(self):
        username = self.user.username

        with allure.step(f'Блокируем пользователя {username}, проверяем статус код'):
            resp = self.api_client.block_user(username)

        with allure.step(f'Проверяем поле status в ответе'):
            assert resp['status'] == 'success'

        with allure.step(f'Проверяем, изменился ли access в бд'):
            assert self.mysql_client.select_user(username).access == 0

        with allure.step(f'Пробуем залогиниться под {username}'):
            resp = self.api_client.post_login(username, self.user.password)
            assert 'Ваша учетная запись заблокирована' in resp.text

    @pytest.mark.API
    def test_unblock_user(self):
        username = self.user.username

        with allure.step(f'Инсертим пользователя {username}, ставим 0 в access'):
            self.mysql_client.update_user(username, access=0)

        with allure.step(f'Разблокируем пользователя {username}, проверяем статус код'):
            resp = self.api_client.unblock_user(username)

        with allure.step(f'Проверяем поле status в ответе'):
            assert resp['status'] == 'success'

        with allure.step(f'Проверяем, изменился ли access в бд'):
            assert self.mysql_client.select_user(username).access == 1


class TestStatusApp(ApiBase):
    @pytest.mark.status
    def test_check_status(self):
        with allure.step(f'Проверяем статус код и поле status'):
            assert self.api_client.check_status()['status'] == 'ok'
