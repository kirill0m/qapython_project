from selenium.webdriver.common.by import By


class LoginPageLocators:
    login = {
        'username': (By.NAME, 'username'),
        'password': (By.ID, 'password')
    }

    LOGIN_BUTTON = (By.ID, 'submit')
    CREATE_ACCOUNT_BUTTON = (By.XPATH, "//a[contains(@href, '/reg')]")

    WARNING_ALERT = (By.XPATH, "//div[contains(@class, 'alert-warning')]")


class RegPageLocators:
    reg = {
        'name': (By.ID, 'user_name'),
        'surname': (By.ID, 'user_surname'),
        'middlename': (By.ID, 'user_middle_name'),
        'email': (By.ID, 'email'),
        'username': (By.NAME, 'username'),
        'password': (By.ID, 'password'),
    }

    PASSWORD_CONFIRM_FIELD = (By.ID, 'confirm')
    CHECKBOX = (By.XPATH, "//input[contains(@type, 'checkbox')]")
    REGISTER_BUTTON = (By.XPATH, "//input[contains(@value, 'Register')]")

    INVALID_FIELD_ALERT = (By.XPATH, "//div[contains(@class, 'alert-danger')]")


class MainPageLocators:
    LOGOUT_BUTTON = (By.ID, 'logout')
    LOGIN_VK_ID = (By.XPATH, "//div[@id='login-name']//ul")
