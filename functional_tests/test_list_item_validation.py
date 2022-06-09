from .base import FunctionalTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from .list_page import ListPage


class ItemValidation(FunctionalTest):
    '''тест валидации элемента списка'''

    def get_error_element(self):
        '''получить элемент с ошибкой'''
        return self.browser.find_element(by=By.CSS_SELECTOR, value='.has-error')

    def test_cannot_add_empty_list_items(self):
        '''тест: нельзя добавлять пустые элементы списка'''
        # Эдит открывает домашнюю страницу и случайно пытается отправить
        # пустой элемент списка. Она нажимает Enter на пустом поле ввода
        self.browser.get(self.live_server_url)
        list_page = ListPage()
        list_page.test = self
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Браузер перехватывает запрос и не загружает страницу со списком
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_text:invalid'))

        # "Эдит начинает набирать текст нового элемента и ошибка исчезает"
        list_page.get_item_input_box().send_keys('Buy milk')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_text:valid'))

        # И она может отправить его успешно
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy milk', 1)

        # Как ни странно, Эдит решает отправить второй пустой элемент списка
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # И снова браузер не подчиняется
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_text:invalid'))

        # И она может исправиться, заполнив поле текстом
        list_page.get_item_input_box().send_keys('Make tea')
        self.wait_for(lambda: self.browser.find_element(by=By.CSS_SELECTOR,
                                                        value='#id_text:valid'))
        list_page.get_item_input_box().send_keys(Keys.ENTER)
        list_page.wait_for_row_in_list_table('Buy milk', 1)
        list_page.wait_for_row_in_list_table('Make tea', 2)

    def test_cannot_add_duplicate_items(self):
        '''тест: нельзя добавлять повторяющиеся элементы'''
        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        list_page = ListPage()
        list_page.test = self
        list_page.add_list_item('Buy wellies')

        # Она случайно пытается ввести повторяющийся элемент
        list_page.get_item_input_box().send_keys('Buy wellies')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        # Она видит полезное сообщение об ошибке
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text.replace('* ', ''),
            "You've already got this in your list"
        ))

    def test_error_message_are_cleared_on_input(self):
        '''тест: сообщения об ошибках очищаются при вводе'''
        # Эдит начинает список и вызывает ошибку валидации
        self.browser.get(self.live_server_url)
        list_page = ListPage()
        list_page.test = self
        list_page.add_list_item('Banter too thick')
        list_page.get_item_input_box().send_keys('Banter too thick')
        list_page.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # Она начинает набирать в поле ввода, чтобы очистить ошибку
        list_page.get_item_input_box().send_keys('a')

        # Она довольна от того, что сообщение исчезает
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
