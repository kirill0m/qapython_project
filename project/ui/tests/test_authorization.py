import pytest
import allure
import errors
from ui.base_ui import BaseUI


class TestAuthorization(BaseUI):
    @pytest.mark.ui_login
    def test_login(self):
        username, password = self.user.username, self.user.password

        with allure.step(f'Заполняем логин/пароль, нажимаем LOGIN'):
            self.login_page.login(username, password)

        with allure.step('Проверяем текущий URL и кнопку Logout'):
            assert self.driver.current_url == self.main_page.url and \
                   self.main_page.find_located(self.main_page.locators.LOGOUT_BUTTON)

    @pytest.mark.ui_login
    @pytest.mark.parametrize(
        'wrong_cred',
        [
            'username',
            'password'
        ]
    )
    def test_login_wrong_creds(self, wrong_cred):
        username, password = self.user.username, self.user.password
        wrong_value = self.builder.generate_value()

        if wrong_cred == 'username':
            username = wrong_value
        else:
            password = wrong_value

        with allure.step('Заполняем логин/пароль, нажимаем LOGIN'):
            self.login_page.login(username, password)

        with allure.step('Проверяем всплывающее сообщение о невалидном логине/пароле'):
            alert = self.login_page.find_visible(self.login_page.locators.WARNING_ALERT)

        assert alert.text == errors.invalid_value_errors['username_password']


class TestsAuthorizationNegative(BaseUI):
    @pytest.mark.ui_login
    @pytest.mark.parametrize(
        'field_length',
        [
            *[{'username': length} for length in [0, 5, 17]],
            *[{'password': length} for length in [0, 5, 21]]
        ]
    )
    def test_login_length(self, field_length):
        """

        """
        name = next(iter(field_length))
        length = next(iter(field_length.values()))

        value = self.builder.generate_value(length)
        user, user_data = self.builder.user(**{name: value})
        field = self.login_page.find_located(self.login_page.locators.login[name])

        with allure.step(f'Проверяем атрибуты поля {name}, мин/макс значения'):
            min, max = self.check_min_max_attrs(name, field)

        with allure.step(f'Проверяем, не попадает ли длина в диапазон'):
            assert not min <= length <= max

        with allure.step('Заполняем логин/пароль, нажимаем LOGIN'):
            self.login_page.login(user.username, user.password)

        if length != 0:
            with allure.step(f'Проверяем всплывающее сообщение о некорректной длине {name}'):
                if length < min:
                    assert errors.invalid_length_errors['any'] in field.get_attribute('validationMessage')
        else:
            with allure.step(f'Проверяем всплывающее сообщение о необходимости заполнить поле'):
                assert field.get_attribute('validationMessage') in errors.empty_field_errors['any']

    @pytest.mark.ui_login
    @pytest.mark.parametrize(
        'field_value',
        [
            *[{'username': type} for type in ['space']],
            *[{'password': type} for type in ['space']]
        ]
    )
    def test_login_value(self, field_value):
        name = next(iter(field_value))
        type = next(iter(field_value.values()))

        value = self.builder.generate_value(value_type=type)

        user, user_json = self.builder.user(**{name: value})

        with allure.step(f'Заполняем логин/пароль, нажимаем LOGIN'):
            self.login_page.login(user.username, user.password)

        with allure.step(f'Проверяем всплывающее сообщение о невалидности значения в поле {name}'):
            alert = self.reg_page.find_visible(self.reg_page.locators.INVALID_FIELD_ALERT).text

            if type == 'space':
                assert alert == errors.empty_field_errors[name]
