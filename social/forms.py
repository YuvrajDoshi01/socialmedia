from django import forms
from .models import Post,Comment

class PostForm(forms.ModelForm):
    caption = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Say something'}))
    class Meta:
        model = Post
        fields = ['caption']                 # Can also add the picture afterwards to make it look like instagram

class CommentForm(forms.ModelForm):
    comment  = forms.CharField(widget = forms.Textarea(attrs = {'placeholder': 'Say something'}))
    class Meta:
        model = Comment
        fields = ['comment']                 
