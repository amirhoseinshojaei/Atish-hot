import uuid

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils import timezone


# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, phone_number, password=None):
        if not username:
            raise ValueError('User name is required')

        if not phone_number:
            raise ValueError('Users must have phone number')

        if not password:
            raise ValueError('Users must have password')

        user = self.model(username=username, phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # SuperUser Section
    def create_superuser(self, username, phone_number, password):
        user = self.create_user(username, phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=50, unique=True)
    regex_phone = RegexValidator(
        regex=r'^09\d{9}$',
        message='Enter a valid phone number like 09.....',

    )
    phone_number = models.CharField(max_length=11, unique=True, validators=[regex_phone])

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone_number']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        db_table = 'users'
        ordering = ['-date_joined']
        get_latest_by = 'date_joined'


    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True





