from django.shortcuts import render ,redirect
from .models import * 
from django.forms import ModelForm ,Textarea
# Create your views here.
def home_view(request):
    posts = Post.objects.all()
    return render(request, "a_posts/home.html",{'posts': posts})


class PostCreateForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        labels = {
            'body':'Caption',
        }
        widgets = {
            'body': Textarea(attrs={'rows': 3,'placeholder':'Add Caption Here ...........','class':'font1 text-4xl'}),
        }

def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, "a_posts/post_create.html",context)