from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CustomUserCreationForm, CommentForm
from .models import Post, Comment, Subscription
from django.views.generic.edit import CreateView

def home(request):
    posts = Post.objects.all()
    context = {'posts': posts, 'user': request.user}
    return render(request, 'home.html', context)

class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'main_app/signup.html'
    success_url = '/create_post/'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

def subpost_detail(request, subpost_name):
    return render(request, 'subpost_detail.html', {'subpost_name': subpost_name})

@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, 'post_detail.html', {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})

# def create_post(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST, request.FILES)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('home')
#         else:
#             print("Form has errors:", form.errors)
#     else:
#         form = PostForm()
    
#     return render(request, 'create_post.html', {'form': form})

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'delete_post.html', {'post': post})

@login_required
def home_feed(request):
    subscribed_subposts = Subscription.objects.filter(user=request.user).values_list('subpost__name', flat=True)
    posts = Post.objects.filter(subpost__name__in=subscribed_subposts)
    return render(request, 'home_feed.html', {'posts': posts})

# @login_required
# def upvote_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.upvotes += 1
#     post.save()
#     return redirect('post_detail', pk=pk)
@login_required
def upvote_post(request, pk):
    if request.is_ajax() and request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.upvotes += 1
        post.save()
        return JsonResponse({"upvotes": post.upvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

# @login_required
# def downvote_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.downvotes += 1
#     post.save()
#     return redirect('post_detail', pk=pk)
@login_required
def downvote_post(request, pk):
    if request.is_ajax() and request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.downvotes += 1
        post.save()
        return JsonResponse({"downvotes": post.downvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
# def upvote_comment(request, post_pk, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     comment.upvotes += 1
#     comment.save()
#     return redirect('post_detail', pk=post_pk)
@login_required
def upvote_comment(request, post_pk, comment_pk):
    if request.is_ajax() and request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.upvotes += 1
        comment.save()
        return JsonResponse({"upvotes": comment.upvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


# @login_required
# def downvote_comment(request, post_pk, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     comment.downvotes += 1
#     comment.save()
#     return redirect('post_detail', pk=post_pk)
@login_required
def downvote_comment(request, post_pk, comment_pk):
    if request.is_ajax() and request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.downvotes += 1
        comment.save()
        return JsonResponse({"downvotes": comment.downvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


def custom_logout(request):
    if request.user.is_authenticated:
        print(f"User {request.user.username} is logging out.")
    logout(request)
    messages.add_message(request, messages.SUCCESS, "You have successfully logged out.")
    return redirect('home')
