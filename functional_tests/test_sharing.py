import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from .base import FunctionalTest


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):
    '''тест обмена данными'''

    def test_can_share_a_list_with_another_user(self):
        '''тест: можно обменитваться списком с ещё одним пользователем'''
        # Эдит является зарегистрированным пользователем
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        self.create_pre_authenticated_sessions(email)
        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Её друг Анцифер тоже зависает на сайте списков
        oni_browser = webdriver.Firefox()
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.browser = oni_browser
        email = 'oniciferous@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)
        self.create_pre_authenticated_sessions(email)

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        self.add_list_item('Get help')

        # Она замечает опцию "Поделиться этим списком"
        share_box = self.browser.find_element(by=By.CSS_SELECTOR,
                                              value='input[name="sharee"]')
        self.assertEqual(share_box.get_attribute('placeholder'),
                         'your-friend@example.com')
