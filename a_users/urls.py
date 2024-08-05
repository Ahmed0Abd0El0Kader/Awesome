from django.urls import path
from .views import *

urlpatterns = [
    path('', profile_view, name='profile'),
    path('<username>', profile_view, name='userprofile'),
    path('edit/', profile_edit_view, name='profile-edit'),
    path('on-boarding/', profile_edit_view, name='profile-onboarding'),
    path('delete/', profile_delete_view, name='profile-delete'), 
]
