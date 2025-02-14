from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from MessangerplusApp import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MessangerplusApp.common.urls')),
    path('accounts/', include('MessangerplusApp.accounts.urls')),
    path('posts/', include('MessangerplusApp.posts.urls')),
    path('chats/', include('MessangerplusApp.chats.urls')),
]

urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
