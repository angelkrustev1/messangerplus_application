from django import template
from MessangerplusApp.posts.models import Post

register = template.Library()


@register.filter
def has_liked(post, user):
    return post.likes.filter(user=user).exists()
