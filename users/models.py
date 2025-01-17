import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
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
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    sur_name = models.CharField(max_length=50, verbose_name=_('Surname'))
    slug = models.SlugField(max_length=40, blank=True)
    email = models.EmailField(max_length=50, unique=True, null=False, blank=False, verbose_name=_('Email'))
    password = models.CharField(max_length=128, null=False, blank=False, verbose_name=_('Password'))
    description = models.TextField(max_length=500, blank=True, verbose_name=_('Description'))
    avatar = models.ImageField(upload_to='authors/', default='authors/default.png', verbose_name=_('Avatar'))
    is_active = models.BooleanField(default=True)
    is_author = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    registered_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'sur_name', 'password']

    def __str__(self):
        return f"{self.first_name} {self.sur_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-id']
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        get_latest_by = 'id'


class Subscription(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name=_('Subscriber'),
                             related_name='subscriber')
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE, verbose_name=_('Subscribed To'),
                               related_name='subscribed_to')
    subscription_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']
        verbose_name = _('Subscription')
        verbose_name_plural = _('Subscriptions')
        get_latest_by = 'id'
        unique_together = ('user', 'author',)
