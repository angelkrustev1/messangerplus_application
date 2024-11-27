from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm

from MessangerplusApp.accounts.models import Profile

UserModel = get_user_model()


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}),
        label='',
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}),
        label='',
    )

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['email'].label = ''


class AppUserAuthenticationForm(AuthenticationForm):
    class Meta:
        model = UserModel

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['password'].label = ''


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_picture', 'biography']

        widgets = {
            'biography': forms.Textarea(
                attrs={'placeholder': 'Biography (optional)'}
            ),
        }

        labels = {
            'biography': '',
            'profile_picture': '',
        }
