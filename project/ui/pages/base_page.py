from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from urllib.parse import urljoin


class BasePage(object):
    base_url = ''

    def __init__(self, driver, location):
        self.driver = driver
        self.url = urljoin(BasePage.base_url, location)

    def get_page(self, location):
        url = urljoin(self.base_url, location)
        self.driver.get(url)

    def wait(self, timeout=None):
        if timeout is None:
            timeout = 5
        return WebDriverWait(self.driver, timeout=timeout)

    def find_located(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.presence_of_element_located(locator))

    def find_visible(self, locator, timeout=None) -> WebElement:
        return self.wait(timeout).until(EC.visibility_of_element_located(locator))

    def click(self, locator, timeout=None) -> WebElement:
        self.find_located(locator, timeout=timeout)
        elem = self.wait(timeout).until(EC.element_to_be_clickable(locator))
        elem.click()

    def fill_out(self, locator, data, timeout=None):
        field = self.find_located(locator, timeout=timeout)
        field.clear()
        field.send_keys(data)
