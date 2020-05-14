from .models import PostComment
from django import forms


class CommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ('name', 'email', 'body')
