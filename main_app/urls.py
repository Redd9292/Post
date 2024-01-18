from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import create_post, edit_post, delete_post, CustomSignUpView, custom_logout

urlpatterns = [
    path('', views.home, name='home'),
    # path('subpost/<slug:subpost_name>/', views.subpost_detail, name='subpost_detail'),
    # path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/upvote/', views.upvote_post, name='upvote_post'),
    path('post/<int:pk>/downvote/', views.downvote_post, name='downvote_post'),
    path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='main_app/login.html'), name='login'),  # Updated line for login
    # path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('logout/', custom_logout, name='logout'),
    path('create_post/', views.create_post, name='create_post'), #added the views
    # path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    # path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
]


