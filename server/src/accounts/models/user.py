from django.db import models
from django.contrib.auth.models import (

    AbstractBaseUser,
    BaseUserManager,
)

from accounts.utils import get_user_upload_image_path


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not password:
            raise ValueError("User must have a password")
        if not email:
            raise ValueError("User must have an email")
        
        email = email.lower()

        user = self.model(
            email=email,
        )
        user.set_password(password)
        user.is_staff = is_staff
        user.is_admin = is_admin
        user.is_active = is_active
        user.save(using=self._db)
        return user
    

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to=get_user_upload_image_path, null=True, blank=True)
    first_name = models.TextField(max_length=25, null=True, blank=True)
    second_name = models.TextField(max_length=25, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        verbose_name = ("User")
        verbose_name_plural = ("Users")

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
