import pytest
import allure
import errors
from ui.base_ui import BaseUI


class TestsUserCreation(BaseUI):
    @pytest.mark.ui_user
    def test_create_user(self, create_user):
        self.login_page.go_to_regpage()

        user, user_json = self.builder.user()

        with allure.step('Заполняем форму регистрации, нажимаем REGISTER'):
            create_user(user.username, user_json)

        with allure.step('Проверяем текущий URL и кнопку Logout'):
            assert self.driver.current_url == self.main_page.url and \
                   self.main_page.find_located(self.main_page.locators.LOGOUT_BUTTON)


class TestsUserCreationNegative(BaseUI):
    @pytest.mark.ui_user
    @pytest.mark.parametrize(
        'field_length',
        [
            *[{'username': length} for length in [0, 5, 17]],
            *[{'password': length} for length in [0, 5, 21]],
            *[{'email': length} for length in [0, 5, 65]]
        ]
    )
    def test_create_user_length(self, field_length):
        """
        Testing length validation of different fields in user creation form
        """
        self.login_page.go_to_regpage()

        name = next(iter(field_length))
        length = next(iter(field_length.values()))

        value = self.builder.generate_email(length) if name == 'email' and length > 4 else self.builder.generate_value(length)
        user, user_json = self.builder.user(**{name: value})
        field = self.reg_page.find_located(self.reg_page.locators.reg[name])

        with allure.step(f'Проверяем атрибуты поля {name}, мин/макс значения'):
            min, max = self.check_min_max_attrs(name, field)

        with allure.step(f'Проверяем, не попадает ли длина в диапазон'):
            assert not min <= length <= max

        with allure.step(f'Заполняем форму регистрации'):
            self.reg_page.fill_user_form(user_json)

        if length != 0:
            with allure.step(f'Нажимаем на REGISTER, проверяем всплывающее сообщение о некорректной длине {name}'):
                if length < min:
                    self.reg_page.submit_and_create()
                    assert bool(v in field.get_attribute('validationMessage') for v in errors.invalid_length_errors['any'])

        else:
            with allure.step(f'Нажимаем на REGISTER'):
                self.reg_page.submit_and_create()

                if self.driver.current_url == self.main_page.url and self.mysql_client.select_user(user.username):
                    self.mysql_client.delete_user(user.username)
                    pytest.fail(f'Пользователь зарегистрирован с {value} в {name}')

                if name == 'email':
                    with allure.step('Проверяем всплывающее сообщение о некорректной длине email'):
                        email_alert = self.reg_page.find_visible(self.reg_page.locators.INVALID_FIELD_ALERT)
                        assert email_alert.text in errors.empty_field_errors['email']
                else:
                    with allure.step('Проверяем всплывающее сообщение о необходимости заполнить поле'):
                        assert field.get_attribute('validationMessage') in errors.empty_field_errors['any']

    @pytest.mark.ui_user
    @pytest.mark.parametrize(
        'field_value',
        [
            *[{'username': type} for type in ['space', 'nums', 'specific', 'all']],
            *[{'password': type} for type in ['space', 'specific']],
            *[{'email': type} for type in ['space', 'nums', 'specific', 'all']]
        ]
    )
    def test_create_user_value(self, field_value):
        """
        Testing validation of different fields in user creation form filling them with different values
        """
        self.login_page.go_to_regpage()

        name = next(iter(field_value))
        type = next(iter(field_value.values()))

        value = self.builder.generate_value(value_type=type)

        user, user_json = self.builder.user(**{name: value})

        with allure.step(f'Заполняем форму регистрации, нажимаем на REGISTER'):
            self.reg_page.fill_user_form(user_json)
            self.reg_page.submit_and_create()

        if self.driver.current_url == self.main_page.url and self.mysql_client.select_user(user.username):
            self.mysql_client.delete_user(user.username)
            pytest.fail(f'Пользователь зарегистрирован с {value} в {name}')

        with allure.step(f'Проверяем всплывающее сообщение о невалидности значения в поле {name}'):
            alert = self.reg_page.find_visible(self.reg_page.locators.INVALID_FIELD_ALERT).text

            if type == 'space':
                assert alert == errors.invalid_value_errors[name] if name == 'email' else errors.empty_field_errors[
                    name]
            else:
                assert alert == errors.invalid_value_errors[name]
