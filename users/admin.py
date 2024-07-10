from django.contrib import admin

from .models import BlogUser, Subscription

admin.site.register(BlogUser)
admin.site.register(Subscription)
