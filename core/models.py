from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError('Users must have phone number')

        if not password:
            raise ValueError('Users must have password')

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # SuperUser Section
    def create_superuser(self, phone_number, password):
        user = self.create_user(phone_number, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
