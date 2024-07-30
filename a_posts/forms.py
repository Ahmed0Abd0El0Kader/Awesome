from django import forms
from .models import *












class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['url','body','tags']
        labels = {
            'body':'Caption',
            'tags':'Category',
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,'placeholder':'Add Caption Here ...........','class':'font1 text-4xl'}),
            'url': forms.TextInput(attrs={'placeholder':'Add URL Here ...........'}),
            'tags':forms.CheckboxSelectMultiple(),
        }

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body','tags']
        labels = {
            'body':'',
            'tags':'Category',

            
        }
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3,'placeholder':'Add Caption Here ...........','class':'font1 text-4xl'}),
            'tags':forms.CheckboxSelectMultiple(),
        }