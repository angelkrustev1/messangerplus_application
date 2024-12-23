from django.contrib import admin
from unfold.admin import ModelAdmin

from MessangerplusApp.chats.models import Message


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ['sender', 'recipient', 'content', 'publication_datetime', 'is_read']
    list_filter = ['is_read', 'publication_datetime']
    search_fields = ['sender__username', 'recipient__username', 'content']
    ordering = ['-publication_datetime']

