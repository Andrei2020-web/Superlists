from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest
from selenium.webdriver.common.by import By

User = get_user_model()


class MyListsTest(FunctionalTest):
    '''тест приложения "Мои списки"'''

    def create_pre_authenticated_sessions(self, email):
        '''создать предварительно аутентифицированный сеанс'''
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()
        ## установить cookie, которые нужны для первого посещения домена.
        ## страницы 404 загружаются быстрее всего!
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/'
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''тест: списки зарегистрированных пользователей
        сохраняются как "мои списки"'''
        email = 'edith@example.com'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Эдит является зарегистрированным пользователем
        self.create_pre_authenticated_sessions(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)

        # Эдит открывает домашнюю страницу и начинает новый список
        self.browser.get(self.live_server_url)
        self.add_list_item('Reticulate splines')
        self.add_list_item('Immanentize eschaton')
        first_list_url = self.browser.current_url

        # Она замечает ссылку на "Мои списки" в первый раз
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT,
                                              value='My lists').click()
        )

        # Она видит, что её список находится там, и он назван
        # на основе первого элемента списка
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT,
                                              value='Reticulate splines')
        )
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Reticulate splines').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, first_list_url)
        )

        # Она решает начать ещё один список, чтобы только убедиться
        self.browser.get(self.live_server_url)
        self.add_list_item('Click cows')
        second_list_url = self.browser.current_url

        # Под заголовком "Мои списки" появляется её новый список
        self.browser.find_element(by=By.LINK_TEXT, value='My lists').click()
        self.wait_for(
            lambda: self.browser.find_element(by=By.LINK_TEXT,
                                              value='Click cows')
        )
        self.browser.find_element(by=By.LINK_TEXT,
                                  value='Click cows').click()
        self.wait_for(
            lambda: self.assertEqual(self.browser.current_url, second_list_url)
        )

        # Она выходит из системы. Опция "Мои списки" исчезает
        self.browser.find_element(by=By.LINK_TEXT, value='Log out').click()
        self.wait_for(
            lambda: self.assertEqual(
                self.browser.find_elements(by=By.LINK_TEXT, value='My lists'),
                [])
        )
