from django.urls import path, include

from MessangerplusApp.common import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-profiles/', views.search_profiles_page, name='search-profiles'),

    path('like/<int:post_pk>/', views.like_functionality, name='like'),
    path('follow/<int:user_pk>/', views.follow_functionality, name='follow'),
    path('comment/<int:post_pk>/', include([
        path('', views.comment_functionality, name='comment'),
        path('<int:comment_pk>/delete/', views.comment_delete, name='comment-delete')
    ])),
]
