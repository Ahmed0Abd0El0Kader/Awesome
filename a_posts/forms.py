from django import forms
from .models import *












class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['url','body']
        labels = {
            'body':'Caption',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,'placeholder':'Add Caption Here ...........','class':'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder':'Add URL Here ...........'}),
        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body']
        labels = {
            'body':'',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,'placeholder':'Add Caption Here ...........','class':'font1 text-4xl'}),}