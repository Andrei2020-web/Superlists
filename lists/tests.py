from django.test import TestCase


class HomePageTest(TestCase):
    '''тест домашней страницы'''

    def test_home_page_returns_correct_html(self):
        '''тест: используется домашний шаблон'''
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_can_save_a_POST_request(self):
        '''тест: можно сохранить post-запрос'''
        responcse = self.client.post('/', data={'item_text': 'A new list item'})
        self.assertIn('A new list item', responcse.content.decode())
        self.assertTemplateUsed(responcse, 'home.html')

