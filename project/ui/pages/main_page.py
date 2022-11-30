from ui.locators.basic_locators import MainPageLocators
from ui.pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver=driver, location='welcome/')

    locators = MainPageLocators

    def logout(self):
        self.click(self.locators.LOGOUT_BUTTON)
