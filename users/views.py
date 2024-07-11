import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

from blog.models import BlogPost
from utils.decorators import LOGOUT_required
from utils.utils import is_valid_email
from .forms import RegisterForm, LoginForm
from .models import BlogUser, Subscription

logger = logging.getLogger("users" + __name__)
contact_logger = logging.getLogger("Contact")

MAX_NAME_LENGTH = 100
MAX_EMAIL_LENGTH = 254
MAX_SUBJECT_LENGTH = 150
MAX_MESSAGE_LENGTH = 2000


@LOGOUT_required
@csrf_protect
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request, request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, _('You have successfully login.'))
                return redirect('home')
            else:
                messages.error(request, _('Incorrect email or password.'))
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


@LOGOUT_required
@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            send_registration_email(user.email, user.first_name, user.sur_name)
            messages.success(request, _('You have successfully registered.'))
            return redirect('home')
    else:
        form = RegisterForm()
    messages.error(request, _('An error occurred during Registration. Please check the input.'))
    return render(request, 'users/register.html', {'form': form})


@login_required
def user_profile(request, slug=None):
    if slug is None:
        return redirect('user_profile', slug=request.user.slug)
    user = get_object_or_404(BlogUser, slug=slug, is_author=True)
    user.blog_post_count = BlogPost.objects.filter(author=user, isPublished=True).count()
    user.last_blog_post = BlogPost.objects.filter(author=user, isPublished=True).order_by('-created_at').first()
    user.subscriber_count = Subscription.objects.filter(author=user).count()
    isSubscribed = Subscription.objects.filter(user=request.user, author=user).exists()
    return render(request, 'users/profile.html', {'user': user, 'isSubscribed': isSubscribed})


def logout_view(request):
    logout(request)
    return redirect('home')


def contact_view(request):  # TODO error message will be fixed
    if request.method == 'POST':
        fields = {
            'name': (request.POST.get('name', ''), MAX_NAME_LENGTH),
            'email': (request.POST.get('email', ''), MAX_EMAIL_LENGTH),
            'subject': (request.POST.get('subject', ''), MAX_SUBJECT_LENGTH),
            'message': (request.POST.get('message', ''), MAX_MESSAGE_LENGTH),
        }
        for field_name, (field_value, max_length) in fields.items():
            if len(field_value) > max_length:
                return JsonResponse({'message': f'{field_name.capitalize()} is too long.'}, status=400)

        if not is_valid_email(email):
            return JsonResponse({'message': 'Invalid email.'}, status=400)

        contact_logger.info(f"User {name}({email}) sent a message with subject: {subject} and message: {message}")

        return JsonResponse({'message': 'Your message has been sent successfully!'})

    return render(request, 'contact.html')


def send_registration_email(user_email, first_name, sur_name):
    # TODO translation here?
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


@login_required
@require_POST
def subscribe_user(request, author_slug):
    user = request.user
    author = get_object_or_404(BlogUser, slug=author_slug)
    if author == user:
        return JsonResponse(status=400, data={'message': 'You cannot subscribe to yourself.'})
    if Subscription.objects.filter(user=user, author=author).exists():
        return JsonResponse(status=400, data={'message': 'You have already subscribed to this author.'})
    Subscription.objects.create(user=user, author=author)
    return JsonResponse(status=200, data={'message': 'You have successfully subscribed to this author.'})


@login_required
@require_POST
def unsubscribe_user(request, author_slug):
    user = request.user
    author = get_object_or_404(BlogUser, slug=author_slug)
    subscription = Subscription.objects.filter(user=user, author=author)
    if not subscription.exists():
        return JsonResponse(status=400, data={'message': 'You are not subscribed to this author.'})
    subscription.delete()
    return JsonResponse(status=200, data={'message': 'You have successfully unsubscribed from this author.'})
