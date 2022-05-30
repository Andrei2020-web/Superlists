from django.urls import re_path
from accounts import views

urlpatterns = [
    # добавлена страница отправки логина на почту пользователя
    re_path(r'^send_login_email$', views.send_login_email, name='send_login_email'),
    # добавлена страница входа в систему
    re_path(r'^login$', views.login, name='login'),
]
