import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Category Name'))

    class Meta:
        ordering = ['-id']
        get_latest_by = 'id'
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    title = models.CharField(max_length=100, verbose_name=_('Title'))
    slug = models.SlugField(max_length=100, blank=True)
    author = models.ForeignKey('users.BlogUser', on_delete=models.CASCADE, verbose_name=_('Author'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Category'))
    content = models.TextField(max_length=50000, verbose_name=_('Content'))
    created_at = models.DateTimeField(auto_now_add=True, editable=False, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    image = models.ImageField(upload_to='blog/', default='blog/default.jpg', verbose_name=_('Image'))
    isPublished = models.BooleanField(default=False, verbose_name=_('Is Published'))
    publish_date = models.DateTimeField(default=None, null=True, verbose_name=_('Publish Date'), blank=True)

    class Meta:
        ordering = ['-id']
        get_latest_by = 'id'
        verbose_name = _('Blog Post')
        verbose_name_plural = _('Blog Posts')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)
