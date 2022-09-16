from datetime import datetime

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Permission,
    PermissionsMixin,
)
from django.core.validators import validate_email
from django.db import models

from forum_comments import validators

# UserManager creates superuser with permissions only to manage usermodel


class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email, username=username, password=password
        )
        user.is_staff = True
        permission = Permission.objects.all().filter(content_type_id=6)
        perm_list = list(permission)
        user.user_permissions.set(perm_list)
        user.save(using=self._db)
        return user


# OrganizationManager creates superuser only to manage organizationmodel


class OrganizationManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        print(email)
        if not email:
            raise ValueError("User must have an email address")
        user = self.model(email=self.normalize_email(email), username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email, username=username, password=password
        )
        user.is_staff = True
        permission = Permission.objects.all().filter(content_type_id=8)
        perm_list = list(permission)
        user.user_permissions.set(perm_list)
        user.save(using=self._db)
        return user


class OrganizationModel(models.Model):
    name = models.CharField(max_length=30)
    NIP = models.CharField(
        max_length=10,
        validators=[
            validators.validate_NIP,
        ],
    )
    country = models.CharField(max_length=30)
    domain_name = models.CharField(
        max_length=30,
        validators=[
            validators.validate_domain,
        ],
    )
    objects = OrganizationManager()

    def __str__(self):
        return self.name


# UserModel inherits from PermissionsMixin for has user.permissions attribute


class UserModel(AbstractBaseUser, PermissionsMixin):
    organization = models.ForeignKey(
        OrganizationModel, blank=True, null=True, on_delete=models.CASCADE
    )
    username = models.CharField(
        max_length=30,
        unique=True,
        error_messages={
            "unique": "User with that username already exists.",
        },
    )
    email = models.EmailField(
        max_length=30,
        unique=True,
        validators=[validate_email],
        error_messages={"unique": "User with that email already exists."},
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "password"]

    def __str__(self):
        return self.username


# Proxy model created to has other user manager(OrganizationManager)
# who create user with other permissions


class OrgUserModel(UserModel):
    objects = OrganizationManager()

    class Meta:
        proxy = True


class Article(models.Model):
    date = models.DateField(auto_now=True)
    image = models.ImageField(null=False, blank=False)
    time = models.DateTimeField(auto_now=True)
    title = models.CharField(
        max_length=30,
        validators=[
            validators.len_title_valid,
        ],
    )
    text = RichTextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    url = models.CharField(max_length=17, unique=True)


class Comment(models.Model):
    date = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)


class PasswordToken(models.Model):
    date = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=150, unique=True)
    username = models.ForeignKey(UserModel, on_delete=models.CASCADE)

    # PasswordToken has classmethod check_token managed by celery in tasks.py

    @classmethod
    def check_token(cls):
        objs = cls.objects.all()
        for obj in objs:
            time = datetime.now() - obj.date.replace(tzinfo=None)
            if time.total_seconds() > 60:
                obj.delete()
                return True
