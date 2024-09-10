from django.http import HttpResponse
from django.shortcuts import render ,redirect ,get_object_or_404
from .models import * 
from bs4 import BeautifulSoup
import requests
from django.contrib import messages
from .forms import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count







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





@login_required
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
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('home')
    context = {'form': form}
    return render(request, "a_posts/post_create.html",context)


@login_required
def post_delete_view(request,id):
    post = get_object_or_404(Post,id = id,author = request.user)
    if request.method == "POST":
        post.delete()
        messages.success(request ,'Post Deleted')
        return redirect('home')
    context = {'post': post}
    return render(request, "a_posts/post_delete.html",context)


@login_required
def post_edit_view(request,id):
    post = get_object_or_404(Post,id = id,author = request.user)

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
    comment_form = CommentCreateForm()
    reply_form = ReplyCreateForm()
    if request.htmx:
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull = False).distinct()
            # comments = comments.order_by('-likes')
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
            
        return render(request,'snippets/loop_postpage_comments.html',{'comments':comments,'replyform': reply_form,})

    
    
    context = {
        'post': post,
        'commentform': comment_form,
        'replyform': reply_form,
        }
    return render(request,'a_posts/post_page.html',context)

@login_required
def comment_sent(request,id):
    post = get_object_or_404(Post,id = id )
    replyform = ReplyCreateForm()
    if request.method == "POST":
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.parent_post = post
            comment.author = request.user
            comment.save()
    return render(request,'snippets/add_comment.html',{'comment':comment,'post':post,'replyform':replyform})

@login_required
def comment_delete_view(request,id):
    comment = get_object_or_404(Comment,id = id,author = request.user)
    if request.method == "POST":
        comment.delete()
        messages.success(request ,'Comment Deleted')
        return redirect('post',comment.parent_post.id)
    context = {'comment': comment}
    return render(request, "a_posts/comment_delete.html",context)

@login_required
def reply_sent(request,id):
    comment = get_object_or_404(Comment,id = id )
    replyform = ReplyCreateForm()
    if request.method == "POST":
        form = ReplyCreateForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.parent_comment = comment
            reply.author = request.user
            reply.save()
    context = {
        'reply':reply,
        'comment':comment,
        'replyform':replyform,
    }        
    return render(request,'snippets/add_reply.html',context)


@login_required
def reply_delete_view(request,id):
    reply = get_object_or_404(Reply,id = id,author = request.user)
    if request.method == "POST":
        reply.delete()
        messages.success(request ,'Reply Deleted')
        return redirect('post',reply.parent_comment.parent_post.id)
    context = {'reply': reply}
    return render(request, "a_posts/reply_delete.html",context)




def like_togggle(model):
    def inner_func(func):
        def wrapper(request,*args,**kwargs):
                obj = get_object_or_404(model,id = kwargs.get('id'))
                user_exist  = obj.likes.filter(username=request.user.username).exists()
                
                if obj.author != request.user :
                    if user_exist:
                        obj.likes.remove(request.user)
                    else:
                        obj.likes.add(request.user)
                return func(request,obj)
        return wrapper
    return inner_func


@login_required
@like_togggle(Post)
def like_post(request,obj):
    return render(request,'snippets/likes.html',{'post':obj})





@login_required
@like_togggle(Comment)
def like_comment(request,obj):
    return render(request,'snippets/likes_comment.html',{'comment':obj})
@login_required
@like_togggle(Reply)
def like_reply(request,obj):
    return render(request,'snippets/likes_reply.html',{'reply':obj})