from behave import given, when, then
from django.conf import settings
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from functional_tests.base import wait

User = get_user_model()


def create_pre_authenticated_session(email):
    user = User.objects.create(email=email)
    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session.save()
    return session.session_key


@wait
def wait_for_list_item(context, item_text):
    context.test.assertIn(
        item_text,
        context.browser.find_element(by=By.CSS_SELECTOR,
                                     value='#id_list_table').text
    )


@given(u'что я являюсь зарегистрированным пользователем')
def given_i_am_logged_in(context):
    '''при условии, что я являюсь зарегистрированным пользователем'''
    session_key = create_pre_authenticated_session(email='edith@example.com')
    ## установить cookie, которые нужны для первого посещения домена.
    ## страница 404 загружается быстрее всего!
    context.browser.get(context.get_url("/404_no_such_url/"))
    context.browser.add_cookie(dict(
        name=settings.SESSION_COOKIE_NAME,
        value=session_key,
        path='/',
    ))


@when(u'я создаю список с первым пунктом "{first_item_text}"')
def create_a_list(context, first_item_text):
    context.browser.get(context.get_url('/'))
    context.browser.find_element(by=By.ID, value='id_text').send_keys(
        first_item_text)
    context.browser.find_element(by=By.ID, value='id_text').send_keys(
        Keys.ENTER)
    wait_for_list_item(context, first_item_text)


@when(u'я добавляю пункт "{item_text}"')
def add_an_item(context, item_text):
    context.browser.find_element(by=By.ID, value='id_text').send_keys(
        item_text)
    context.browser.find_element(by=By.ID, value='id_text').send_keys(
        Keys.ENTER)
    wait_for_list_item(context, item_text)


@then(u'я увижу ссылку на "{link_text}"')
@wait
def see_a_link(context, link_text):
    context.browser.find_element(by=By.LINK_TEXT, value=link_text)


@when(u'я нажимаю на ссылку "{link_text}"')
def click_link(context, link_text):
    context.browser.find_element(by=By.LINK_TEXT, value=link_text).click()


@then(u'я окажусь на странице списка "{first_item_text}"')
@wait
def on_list_page(context, first_item_text):
    first_row = context.browser.find_element(
        by=By.CSS_SELECTOR,
        value='#id_list_table tr:first-child'
    )
    expected_row_text = '1: ' + first_item_text
    context.test.assertEqual(first_row.text, expected_row_text)