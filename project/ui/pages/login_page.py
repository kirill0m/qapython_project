from ui.locators.basic_locators import LoginPageLocators
from ui.pages.base_page import BasePage
from ui.pages.main_page import MainPage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver=driver, location='login')
        self.get_page(self.url)

    locators = LoginPageLocators

    def go_to_regpage(self):
        self.click(self.locators.CREATE_ACCOUNT_BUTTON)

    def login(self, username, password):
        self.fill_out(self.locators.login['username'], username)
        self.fill_out(self.locators.login['password'], password)
        self.click(self.locators.LOGIN_BUTTON)
        return MainPage(self.driver)
