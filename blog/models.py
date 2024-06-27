from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from djangoblog.utils import get_current_site
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    color_code = models.CharField(max_length=7, default='#000000')

    class Meta:
        ordering = ['-id']
        get_latest_by = 'id'
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    author = models.ForeignKey('users.Author', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        get_latest_by = 'id'
        verbose_name = 'blog post'
        verbose_name_plural = 'blog posts'

    def __str__(self):
        return self.title
