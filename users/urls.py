from django.urls import path
from .views import register, user_login, logout_view, activate_subscribe, deactivate_subscribe

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', logout_view, name='logout'),
    path('activate-subscribe/', activate_subscribe, name='activate_subscribe'),
    path('deactivate-subscribe/', deactivate_subscribe, name='deactivate_subscribe'),
]
