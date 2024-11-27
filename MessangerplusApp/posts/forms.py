from django import forms

from MessangerplusApp.posts.models import Post


class PostBaseForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['user']
        abstract = True

        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Description (optional)'}),
        }

        labels = {
            'photo': '',
            'title': '',
            'description': ''
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['description'].required = False


class PostCreationForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['photo', 'title', 'description']


class PostEditForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        fields = ['title', 'description']


class PostDeleteForm(PostBaseForm):
    class Meta(PostBaseForm.Meta):
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
