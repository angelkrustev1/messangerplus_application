from django.contrib.auth import get_user_model
from django.db import models


UserModel = get_user_model()


class Message(models.Model):
    class Meta:
        permissions = [
            ('can_administer_messages', 'Can administer all messages'),
        ]

        indexes = [
            models.Index(fields=['publication_datetime']),
            models.Index(fields=['is_read']),
            models.Index(fields=['sender', 'recipient']),
        ]

        ordering = ['publication_datetime']

    sender = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )

    recipient = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='received_messages',
    )

    content = models.TextField(
        max_length=700,
    )

    publication_datetime = models.DateTimeField(
        auto_now_add=True,
        blank=True,
    )

    is_read = models.BooleanField(
        default=False,
        blank=True,
    )

    def __str__(self):
        return f'Message from {self.sender} to {self.recipient} at {self.publication_datetime}'
