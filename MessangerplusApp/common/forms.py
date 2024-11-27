from django import forms

from MessangerplusApp.common.models import Comment


class SearchForm(forms.Form):
    query = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Search',
            }
        ),
        label='',
        required=False,
    )


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

        widgets = {
            'content': forms.TextInput(
                attrs={'placeholder': 'Write a comment...'}
            )
        }

        labels = {
            'content': '',
        }
