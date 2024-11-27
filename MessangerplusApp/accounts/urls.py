from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path, include

from MessangerplusApp.accounts import views

urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('login/', views.AppUserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('user/<int:pk>/delete', views.user_delete, name='user-delete'),
    path('profile/', include([
        path('<int:pk>/', views.profile_details, name='profile-details'),
        path('<int:pk>/edit/', views.profile_edit, name='profile-edit'),
        path('<int:pk>/delete/', views.profile_delete, name='profile-delete'),
        path('<int:pk>/following/', views.profile_following, name='profile-following'),
        path('<int:pk>/followers/', views.profile_followers, name='profile-followers'),
    ]))
]
