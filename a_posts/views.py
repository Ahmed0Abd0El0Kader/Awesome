from django.shortcuts import render ,redirect ,get_object_or_404
from .models import * 
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import *








def home_view(request,tag = None):
    if tag :
        posts = Post.objects.filter(tags__slug = tag)
        tag = get_object_or_404(Tag,slug = tag)
    else:
        posts = Post.objects.all()
    categories =  Tag.objects.all()   
    context = {
        'posts' : posts,
        'categories' : categories ,
        'tag' : tag ,
    }    
    return render(request, "a_posts/home.html",context)






def post_create_view(request):
    form = PostCreateForm()
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text,'html.parser')
            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            image = find_image[0]['content']
            post.image = image
            
            find_title = sourcecode.select('h1.photo-title')
            title = find_title[0].text.strip()
            post.title = title
            
            find_title = sourcecode.select('a.owner-name')             
            artist = find_title[0].text.strip()
            post.artist = artist
            
            post.save()
            form.save_m2m()
            return redirect('home')
    context = {'form': form}
    return render(request, "a_posts/post_create.html",context)



def post_delete_view(request,id):
    post = get_object_or_404(Post,id = id)
    if request.method == "POST":
        post.delete()
        messages.success(request ,'Post Deleted')
        return redirect('home')
    context = {'post': post}
    return render(request, "a_posts/post_delete.html",context)


def post_edit_view(request,id):
    post = get_object_or_404(Post,id = id)
    form = PostEditForm(instance=post)
    if request.method == 'POST':
        form = PostEditForm(request.POST,instance=post)
        if form.is_valid():
            form.save()
            messages.success(request,'Post Updated')
            return redirect('home')
    context = {'post': post,
               'form':form,}
    return render(request, "a_posts/post_edit.html",context)

def post_page_view(request,id):
    post = get_object_or_404(Post,id = id)
    context = {'post': post}
    return render(request,'a_posts/post_page.html',context)
