from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from .base import wait


class ListPage():
    '''страница списка'''

    def get_table_row(self):
        '''получить строки таблицы'''
        return self.test.browser.find_elements(by=By.CSS_SELECTOR,
                                               value='#id_list_table tr')

    @wait
    def wait_for_row_in_list_table(self, item_text, item_number):
        row_text = '{}: {}'.format(item_number, item_text)
        rows = self.get_table_row()
        self.test.assertIn(row_text, [row.text for row in rows])

    def get_item_input_box(self):
        '''получить поле ввода для элемента'''
        return self.test.browser.find_element(by=By.ID, value='id_text')

    def add_list_item(self, item_text):
        '''добавить элемент списка'''

        self.get_item_input_box().send_keys(item_text)
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.browser.find_element(by=By.ID,
                                                                  value='id_list_table'))
        num_rows = len(self.get_table_row())
        self.wait_for_row_in_list_table(item_text, num_rows)
        return self

    def get_share_box(self):
        '''получить поле для обмена списками'''
        return self.test.browser.find_element(by=By.CSS_SELECTOR,
                                              value='input[name="share"]')

    def get_shared_with_list(self):
        '''получить список от того, кто им делится'''
        return self.test.browser.find_elements(by=By.CSS_SELECTOR,
                                               value='.list-sharee')

    def share_list_with(self, email):
        '''поделиться списком с '''
        self.get_share_box().send_keys(email)
        self.get_share_box().send_keys(Keys.ENTER)
        self.test.wait_for(lambda: self.test.assertIn(
            email,
            [item.text for item in self.get_shared_with_list()]
        ))

    def get_list_owner(self):
        '''получить владельца списка'''
        return self.test.browser.find_element(by=By.ID,
                                              value='id_list_owner').text
