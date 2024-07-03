from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_admin=True.')
        return self.create_user(email, password, **extra_fields)


class BlogUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    sur_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False)
    password = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField(max_length=200, blank=True)
    avatar = models.ImageField(upload_to='static/authors/', default='static/authors/default.png')
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'sur_name', 'password']

    def __str__(self):
        return f"{self.first_name} {self.sur_name}"

    class Meta:
        ordering = ['-id']
        verbose_name = _('user')
        verbose_name_plural = _('users')
        get_latest_by = 'id'
