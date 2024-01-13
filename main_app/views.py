from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm
# from django.contrib.auth.views import SignUpView

# from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'home.html')

def my_protected_view(request):
    return render(request, 'my_protected_view.html')

# class CustomSignUpView(SignUpView):
#     form_class = CustomUserCreationForm
#     template_name = 'signup.html'

def subpost_detail(request, subpost_name):
    return render(request, 'subpost_detail.html', {'subpost_name': subpost_name})

def post_detail(request, post_id):
    return render(request, 'post_detail.html', {'post_id': post_id})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request,POST, instance=post)
        form.save()
        return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})