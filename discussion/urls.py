from django.urls import path
from discussion import views
from .views import CreatePost, DiscussionAllData, UpdatePost, CreateComment, UpdateComment

urlpatterns = [
    path('postlist/<str:pk>', DiscussionAllData().as_view(), name='postlist'),
    path('createpost', CreatePost.as_view(), name='createpost'),
    path('updatepost/<str:pk>', UpdatePost().as_view(), name='updatepost'),
    path('deletepost/<str:pk>', views.discussionDelete, name='deletepost'),
    path('commentlist', views.commentList, name='commentlist'),
    path('createcomment', CreateComment().as_view(), name='createcomment'),
    path('editcomment/<str:pk>', UpdateComment.as_view(), name='editcomment'),
    path('deletecomment/<str:pk>', views.commentDelete, name='deletecomment'),
    path('likelist', views.likeList, name='likelist'),
    path('editlike', views.likeEdit, name='editlike'),
]
