
from django.contrib import admin
from django.urls import path ,include
from a_posts.views import * 
from a_users.views import * 
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('a_posts.urls')),
    path('profile/', include('a_users.urls')),
    

    
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)