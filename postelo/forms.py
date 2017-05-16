from django import forms
from .models import Message


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        exclude = ('sender', 'draft', 'is_read', 'time_stamp', 'is_trash')
