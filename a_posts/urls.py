from django.urls import path
from . views import *

app_name = 'a_posts'

urlpatterns = [
    path('', home_view,name='home'),
    path('category/<tag>/', home_view,name="category"),
    path('post/create/', post_create_view,name="post-create"),
    path('post/delete/<id>/', post_delete_view,name="post-delete"),
    path('post/edit/<id>/', post_edit_view,name="post-edit"),
    path('post/page/<id>/', post_page_view,name="post"),
]
