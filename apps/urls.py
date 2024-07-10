"""
URL configuration for ayvblog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from users.views import contact_view, user_profile
from users.views import subscribe_user, unsubscribe_user
from .views import set_language

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("blog.urls")),
    path("profile/<slug:slug>/", user_profile, name="user_profile"),
    path("profile/", user_profile, name="user_main_profile"),
    path("auth/", include("users.urls")),
    path('contact/', contact_view, name='contact'),
    path('set_language/<str:language_code>/', set_language, name='set_language'),
    path('subscribe/<slug:author_slug>/', subscribe_user, name='subscribe_user'),
    path('unsubscribe/<slug:author_slug>/', unsubscribe_user, name='unsubscribe_user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
