from django.shortcuts import render,redirect ,get_object_or_404
from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from . models import *
from .forms import * 

def profile_view(request,username = None):
    if username :
        profile = get_object_or_404(User,username = username).profile
    else:    
        try:
            profile = request.user.profile
        except:
            raise Http404()
    context = {
        'profile' : profile
    }
    return render(request,'a_users/profile.html',context)

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    if request.path ==  reverse('profile-onboarding'):
        template = 'a_users/profile_onboarding.html'   
        
    else: 
        template =  'a_users/profile_edit.html'   
    context = {
        'form' : form
    }    
    return render(request,template,context)



@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()        
        messages.success(request,"Account Deleted  " )
        return redirect('a_posts:home')
    return render(request,'a_users/profile_delete.html')