from django.shortcuts import render
from django.core.mail import send_mail
from django.shortcuts import redirect
from accounts.models import Token
from django.urls import reverse
from django.contrib import auth, messages


# Create your views here.
def send_login_email(request):
    '''отправить сообщение для входа в систему'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'fortestpostsend@mail.ru',
        [email]
    )
    messages.add_message(
        request,
        messages.SUCCESS,
        "Проверьте свою почту, мы отправили Вам ссылку, "
        "которую можно использовать для входа на сайт."
    )
    return redirect('/')


def login(request):
    '''зарегистрировать вход в систему'''
    user = auth.authenticate(request=request, uid=request.GET.get('token'))
    if user:
        auth.login(request, user)
    return redirect('/')
