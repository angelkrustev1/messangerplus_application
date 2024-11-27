from django.contrib import admin

from MessangerplusApp.common.models import Comment, Like


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'to_post', 'content', 'publication_datetime']
    list_filter = ['publication_datetime', 'user', 'to_post']
    search_fields = ('user__username', 'to_post__description')
    ordering = ('-publication_datetime',)


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'to_post']
    list_filter = ['user', 'to_post']
    search_fields = ['user__username', 'to_post__description']