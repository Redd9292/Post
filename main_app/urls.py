from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_post, edit_post, delete_post, CustomSignUpView, custom_logout

urlpatterns = [
    path('', views.home, name='home'),
   
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
   
    path('post/<int:post_id>/add_photo/', views.add_photo, name='add_photo'),
    path('post/<int:delete_id>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:upvote_id>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:downvote_id>/downvote/', views.downvote_post, name='downvote_post'),
    path('upvote-comment/<int:comment_id>/', views.upvote_comment, name='upvote_comment'),
    path('downvote-comment/<int:comment_id>/', views.downvote_comment, name='downvote_comment'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='main_app/login.html'), name='login'),
    path('logout/', custom_logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'), 
    path('create_post/<int:create_id>/', views.create_post, name='post'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
]


