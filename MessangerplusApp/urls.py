from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from MessangerplusApp import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('MessangerplusApp.common.urls')),
    path('accounts/', include('MessangerplusApp.accounts.urls')),
    path('posts/', include('MessangerplusApp.posts.urls')),
    path('chats/', include('MessangerplusApp.chats.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
