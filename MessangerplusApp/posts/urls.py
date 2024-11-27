from django.urls import path, include

from MessangerplusApp.posts import views

urlpatterns = [
    path('', views.posts_for_you_page, name='posts-for-you'),
    path('create/', views.create_post, name='create-post'),
    path('post/', include([
        path('<int:post_pk>/', views.post_details, name='post-details'),
        path('<int:post_pk>/edit/', views.post_edit, name='post-edit'),
        path('<int:post_pk>/delete/', views.post_delete, name='post-delete'),
    ]))
]