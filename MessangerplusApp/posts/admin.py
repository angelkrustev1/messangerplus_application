from django.contrib import admin
from unfold.admin import ModelAdmin

from MessangerplusApp.posts.models import Post


@admin.register(Post)
class PostAdmin(ModelAdmin):
    list_display = ['title', 'user', 'description', 'publication_datetime']
    list_filter = ['publication_datetime', 'user']
    search_fields = ['user__username', 'title', 'description']
    ordering = ['-publication_datetime', 'title']
