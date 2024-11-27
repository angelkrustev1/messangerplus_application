from django import forms

from MessangerplusApp.chats.models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        widgets = {
            'content': forms.TextInput(
                attrs={'placeholder': 'Write a message...'}
            )
        }

        labels = {
            'content': '',
        }

