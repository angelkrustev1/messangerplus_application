from django.urls import path, include

from MessangerplusApp.chats import views

urlpatterns = [
    path('', views.chats_page, name='chats'),
    path('chat/<int:pk>/', include([
        path('', views.chat_one_on_one, name='chat-one-on-one'),
        path('<int:message_pk>/delete', views.message_delete, name='message-delete'),
    ])),
]