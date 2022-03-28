from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    body=forms.CharField(
       label='',
       widget=forms.Textarea(attrs={
           'rows':'1',
           'placeholder':'Say something...'
        })
    )

    
    class Meta:
        model=Comment
        fields=['body']