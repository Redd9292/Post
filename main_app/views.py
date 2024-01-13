from django.shortcuts import render, redirect
from .forms import PostForm

def home(request):
    return render(request, 'home.html')

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