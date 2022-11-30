from ui.locators.basic_locators import RegPageLocators
from ui.pages.base_page import BasePage


class RegPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver=driver, location='reg')

    locators = RegPageLocators

    def fill_user_form(self, user_data):
        self.fill_out(self.locators.reg['name'], user_data['name'])
        self.fill_out(self.locators.reg['surname'], user_data['surname'])
        self.fill_out(self.locators.reg['middlename'], user_data['middle_name'])
        self.fill_out(self.locators.reg['email'], user_data['email'])
        self.fill_out(self.locators.reg['username'], user_data['username'])
        self.fill_out(self.locators.reg['password'], user_data['password'])
        self.fill_out(self.locators.PASSWORD_CONFIRM_FIELD, user_data['password'])

    def submit_and_create(self):
        self.click(self.locators.CHECKBOX)
        self.click(self.locators.REGISTER_BUTTON)
