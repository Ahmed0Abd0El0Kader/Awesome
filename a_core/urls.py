
from django.contrib import admin
from django.urls import path ,include
from a_posts.views import * 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view,name='home'),
    path('category/<tag>/', home_view,name="category"),
    path('post/create/', post_create_view,name="post-create"),
    path('post/delete/<id>/', post_delete_view,name="post-delete"),
    path('post/edit/<id>/', post_edit_view,name="post-edit"),
    path('post/page/<id>/', post_page_view,name="post"),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)