from django.contrib import admin
from django.urls import path
from .views import AddFollower, DisLike,AddLike,PostListView,PostDetailView,PostEditView,PostDeleteView,CommentDeleteView, ProfileEditView, ProfileView,RemoveFollower,PostAddView

urlpatterns = [
    path('',PostListView.as_view(),name= 'post-list'),
    path('post/add_post', PostAddView.as_view(),name ='post-add'),
    path('post/<int:pk>',PostDetailView.as_view(),name = 'post-detail'),
    path('post/edit/<int:pk>',PostEditView.as_view(),name = 'post-edit'),
    path('post/delete/<int:pk>',PostDeleteView.as_view(),name = 'post-delete'),
    path('post/<int:post_pk>/comment-delete/<int:pk>',CommentDeleteView.as_view(),name = 'comment-delete'),
    path('profile/<int:pk>',ProfileView.as_view(),name = 'profile'),
    path('profile/edit/<int:pk>',ProfileEditView.as_view(),name = 'profile-edit'),
    path('profile/<int:pk>/followers/add',AddFollower.as_view(),name = 'add-followers'),
    path('profile/<int:pk>/followers/remove',RemoveFollower.as_view(),name = 'remove-followers'),
    path('post/<int:pk>/like',AddLike.as_view(),name='like'),
    path('post/<int:pk>/dislike',DisLike.as_view(),name='dislike')
]
