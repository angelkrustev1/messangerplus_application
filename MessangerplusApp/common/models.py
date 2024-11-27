from django.contrib.auth import get_user_model
from django.db import models

from MessangerplusApp.posts.models import Post

UserModel = get_user_model()


class Comment(models.Model):
    class Meta:
        permissions = [
            ('can_administer_comments', 'Can administer all comments'),
        ]

        indexes = [
            models.Index(
                fields=['publication_datetime']
            )
        ]

        ordering = ['-publication_datetime']

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
    )

    content = models.TextField(
        max_length=350,
    )

    publication_datetime = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )


class Like(models.Model):
    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='likes',
    )

    to_post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='likes',
    )
