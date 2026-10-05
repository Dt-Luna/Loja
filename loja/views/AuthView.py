from urllib.parse import urlencode

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme

from loja.forms.AuthForm import LoginForm, RegisterForm


def _redirect_after_auth(request, default_url='/'):
    next_url = request.POST.get('next') or request.GET.get('next') or default_url
    if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
        return redirect(next_url)
    return redirect(default_url)


def login_view(request):
    next_url = request.GET.get('next') or '/'
    if request.user.is_authenticated:
        return redirect(next_url if next_url.startswith('/') else '/')

    login_form = LoginForm()
    message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return _redirect_after_auth(request, '/')
            message = {'type': 'danger', 'text': 'Usuário ou senha inválidos.'}

    context = {
        'form': login_form,
        'message': message,
        'title': 'Login',
        'button_text': 'Entrar',
        'link_text': 'Registrar',
        'link_href': f"{reverse('register')}?{urlencode({'next': next_url})}",
        'next': next_url,
    }
    return render(request, template_name='auth/auth.html', context=context, status=200)


def register_view(request):
    next_url = request.GET.get('next') or '/'
    register_form = RegisterForm()
    message = None

    if request.user.is_authenticated:
        return redirect(next_url if next_url.startswith('/') else '/')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        register_form = RegisterForm(request.POST)

        if register_form.is_valid():
            verify_username = User.objects.filter(username=username).first()
            verify_email = User.objects.filter(email=email).first()

            if verify_username is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este username!'}
            elif verify_email is not None:
                message = {'type': 'danger', 'text': 'Já existe um usuário com este e-mail!'}
            else:
                user = User.objects.create_user(username, email, password)
                if user is not None:
                    message = {'type': 'success', 'text': 'Conta criada com sucesso!'}
                    if next_url and next_url.startswith('/'):
                        return redirect(f"{reverse('login')}?{urlencode({'next': next_url})}")
                    return redirect('login')
                message = {'type': 'danger', 'text': 'Um erro ocorreu ao tentar criar o usuário.'}

    context = {
        'form': register_form,
        'message': message,
        'title': 'Registrar',
        'button_text': 'Registrar',
        'link_text': 'Login',
        'link_href': f"{reverse('login')}?{urlencode({'next': next_url})}",
        'next': next_url,
    }
    return render(request, template_name='auth/auth.html', context=context, status=200)


def logout_view(request):
    logout(request)
    return redirect('login')
