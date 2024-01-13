from django.urls import path
from .import views
from .views import create_post, edit_post, delete_post

urlpatterns = [
    path('', views.home, name='home'),
    path('subpost/<slug:subpost_name>/', views.subpost_detail, name='subpost_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
]
