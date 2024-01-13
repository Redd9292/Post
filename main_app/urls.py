from django.urls import path
from .import views
from .views import create_post, edit_post, delete_post, my_protected_view
# from .views import CustomSignUpView

urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('signup/', auth_views.SignupView.as_view(template_name='signup.html'), name='signup'),\
    # path('signup/', CustomSignUpView.as_view(), name='signup'),
    path('my_protected_view/', my_protected_view, name='my_protected_view'),
    path('subpost/<slug:subpost_name>/', views.subpost_detail, name='subpost_detail'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('create_post/', create_post, name='create_post'),
    path('edit_post/<int:post_id>/', edit_post, name='edit_post'),
    path('delete_post/<int:post_id>/', delete_post, name='delete_post'),
]
