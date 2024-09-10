from django.urls import path
from . views import *


urlpatterns = [
    path('', home_view,name='home'),
    path('category/<tag>/', home_view,name="category"),
    path('post/create/', post_create_view,name="post-create"),
    path('post/delete/<id>/', post_delete_view,name="post-delete"),
    path('post/edit/<id>/', post_edit_view,name="post-edit"),
    path('post/page/<id>/', post_page_view,name="post"),
    path('post/<id>/like/', like_post,name="like-post"),
    path('commentsent/<id>/', comment_sent,name="comment-sent"),
    path('comment/delete/<id>/', comment_delete_view,name="comment-delete"),
    path('comment/like/<id>/', like_comment,name="like-comment"),
    path('replysent/<id>/', reply_sent,name="reply-sent"),
    path('reply/delete/<id>/', reply_delete_view,name="reply-delete"),
    path('reply/like/<id>/', like_reply,name="like-reply"),
]
