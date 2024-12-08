from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','parent']
        widgets = {'parent': forms.HiddenInput()}