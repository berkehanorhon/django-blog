from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    first_name = models.CharField(max_length=50, blank= True)
    sur_name = models.CharField(max_length=50, blank= True)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=16, unique=True, null=False, blank=False)
    description = models.TextField(max_length=200)

    def __str__(self):
        return "%s %s" % (self.first_name, self.sur_name)

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = verbose_name
        get_latest_by = 'id'
