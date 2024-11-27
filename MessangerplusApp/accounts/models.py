from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

from MessangerplusApp.accounts.managers import AppUserManager
from MessangerplusApp.accounts.validators import validate_picture_size


class AppUser(AbstractBaseUser, PermissionsMixin):
    class Meta(AbstractBaseUser.Meta):
        permissions = [
            ('can_administer_profiles', 'Can administer all profiles'),
        ]

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[username_validator],
    )

    email = models.EmailField()

    date_joined = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = AppUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username


UserModel = get_user_model()


class Profile(models.Model):

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    biography = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        validators=[
            validate_picture_size,
        ],
        blank=True,
        null=True,
    )

    following = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='followers',
        blank=True,
    )

    def __str__(self):
        return f'Profile of {self.user.username}'
