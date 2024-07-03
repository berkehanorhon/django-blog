from .forms import RegisterForm, LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Başarıyla giriş yaptınız.')
                return redirect('home')
            else:
                messages.error(request, 'Geçersiz kullanıcı adı veya şifre.')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_registration_email(user.email, user.first_name, user.sur_name)
            messages.success(request, 'Başarıyla kayıt oldunuz.')
            return redirect('home')
    else:
        form = RegisterForm()
    messages.error(request, 'Kayıt işlemi sırasında hata! Lütfen tekrar deneyiniz.')
    return render(request, 'users/register.html', {'form': form})


def send_registration_email(user_email, first_name, sur_name):
    subject = "Welcome to AyvBlog!"
    html_message = render_to_string('register_email.html',
                                    {'user_email': user_email, 'first_name': first_name, 'sur_name': sur_name})
    recipient_list = [user_email, ]
    try:
        send_mail(
            subject=subject,
            html_message=html_message,
            message="Welcome to AyvBlog!",
            recipient_list=recipient_list,
            from_email="AyvBlog",
            fail_silently=False,
        )
    except Exception as e:
        print(e)
