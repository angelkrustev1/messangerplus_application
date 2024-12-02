from django.contrib import admin
from django.contrib.auth import get_user_model
from unfold.admin import ModelAdmin

from MessangerplusApp.accounts.forms import AppUserCreationForm, AppUserChangeForm
from MessangerplusApp.accounts.models import Profile

UserModel = get_user_model()


@admin.register(UserModel)
class AppUserAdmin(ModelAdmin):
    model = UserModel
    add_form = AppUserCreationForm
    form = AppUserChangeForm

    list_display = ['username', 'email', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email']
    ordering = ['username', '-date_joined']

    fieldsets = [
        [
            None,
            {'fields': ['username', 'email', 'password']}
        ],
        [
            'Permissions',
            {'fields': ['is_active', 'is_staff', 'groups', 'user_permissions']}
        ],
        [
            'Important dates',
            {'fields': ['last_login']}
        ]
    ]

    add_fieldsets = [
        [
            None,
            {
                'classes': ['wide'],
                'fields': {'username', 'email', 'password'}
            }
        ],
    ]


@admin.register(Profile)
class ProfileAdmin(ModelAdmin):
    list_display = ['user', 'biography']
    search_fields = ['user__username', 'user__email', 'biography']
    list_filter = ['user__is_active', 'user__is_staff', 'user__date_joined']
    ordering = ['user__username', '-user__date_joined']

    fieldsets = [
        [
            None,
            {'fields': ['user', 'biography', 'profile_picture']}
        ],
        [
            'Relationships',
            {'fields': ['following']}
        ]
    ]
