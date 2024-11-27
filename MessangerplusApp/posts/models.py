from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from MessangerplusApp.posts.validators import validate_picture_size

UserModel = get_user_model()


class Post(models.Model):
    class Meta:
        permissions = [
            ('can_administer_posts', 'Can administer all posts'),
        ]

        indexes = [
            models.Index(fields=['publication_datetime']),
        ]

        ordering = ['-publication_datetime']

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='posts',
    )

    photo = models.ImageField(
        upload_to='posts/',
        validators=[
            validate_picture_size
        ],
    )

    title = models.CharField(
        max_length=100,
    )

    description = models.TextField(
        max_length=500,
        validators=[
            MinLengthValidator(3),
        ],
        null=True,
        blank=True,
    )

    publication_datetime = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )


