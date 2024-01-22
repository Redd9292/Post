import os
import uuid
import boto3
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Photo
from django.http import JsonResponse
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import PostForm, CustomUserCreationForm, CommentForm, PhotoForm
from .models import Post, Comment, Subscription, Photo
from django.views.generic.edit import CreateView, UpdateView


def some_function(request):
    secret_key = os.environ['SECRET_KEY']
    
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

# @login_required
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comments.all()
#     # new_comment = None

#     if request.method == 'POST':
#         comment_form = CommentForm(data=request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.author = request.user
#             new_comment.post = post
#             new_comment.save()
#     else:
#         comment_form = CommentForm()

#     return render(request, 'post_detail.html', {
#         'post': post,
#         'comments': comments,
#         'new_comment': new_comment,
#         'comment_form': comment_form
#     })


# If login is required to post comments, uncomment the next line
# @login_required
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)

#     # Fetch comments here if not submitting a form, or after saving a comment
#     comments = post.comments.all()  # Assuming 'comments' is the related_name in your Comment model

#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post

#             # Check if the Comment model has an author field and user is authenticated
#             if hasattr(new_comment, 'author') and request.user.is_authenticated:
#                 new_comment.author = request.user

#             new_comment.save()

#             # Fetch comments again to include the new comment
#             comments = post.comments.all()

#             # Redirecting to the same page to display the updated list of comments
#             return redirect('post_detail', pk=post.pk)
#     else:
#         comment_form = CommentForm()

#     context = {
#         'post': post,
#         'comments': comments,
#         'comment_form': comment_form
#     }

#     return render(request, 'post_detail.html', context)


@login_required  # Optional: Use if you want only authenticated users to comment
def post_detail(request, post_id):
    # post = get_object_or_404(Post, pk=pk)
    post = Post.objects.get(id = post_id)
    comments = post.comments.all()

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = request.user  # Get the logged-in user
            new_comment.save()
            return redirect('post_detail', post_id = post_id)  # Redirect back to the post detail page
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }
    print('comment',comment_form)
    return render(request, 'post_detail.html', context)



# @login_required  # Add this if you want to restrict access to authenticated users only
# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     comments = post.comments.all()

#     if request.method == 'POST':
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.author = request.user.username  # Use the username of the logged-in user
#             new_comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         comment_form = CommentForm()

#     context = {
#         'post': post,
#         'comments': comments,
#         'comment_form': comment_form
#     }
#     return render(request, 'post_detail.html', context)



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save()
            # Handle the photo upload
            photo = request.FILES.get('photo')
            if photo:
                Photo.objects.create(post=new_post, image=photo)  # Adjust according to your Photo model fields
            return redirect('home')  # Redirect to a success page or the detail view of the post
            
    else:
        form = PostForm()

    return render(request, 'create_post.html', {'form': form})

# EDIT START
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        # Redirect or show error if the user is not the owner
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect('post_detail', pk=pk)

    if request.method == 'POST':
        post.delete()
        return redirect('home')

    return render(request, 'confirm_delete_post.html', {'post': post})

@login_required
def edit_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=comment.post.pk)
    else:
        form = CommentForm(instance=comment)

    return render(request, 'edit_comment.html', {'form': form})

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user != comment.author:
        return redirect('post_detail', pk=comment.post.pk)

    if request.method == 'POST':
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)

    return render(request, 'confirm_delete_comment.html', {'comment': comment})
#    EDIT END

@login_required
def home_feed(request):
    subscribed_subposts = Subscription.objects.filter(user=request.user).values_list('subpost__name', flat=True)
    posts = Post.objects.filter(subpost__name__in=subscribed_subposts)
    return render(request, 'home_feed.html', {'posts': posts})

# @login_required
# def upvote_post(request, pk):
#     if request.is_ajax() and request.method == "POST":
#         post = get_object_or_404(Post, pk=pk)
#         post.upvotes += 1
#         post.save()
#         return JsonResponse({"upvotes": post.upvotes})
#     else:
#         return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def upvote_post(request, pk):
    if request.is_ajax() and request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        # Check if user has already upvoted
        if request.user in post.upvoted_users.all():
            # User is removing their upvote
            post.upvoted_users.remove(request.user)
            post.upvotes -= 1
        elif request.user in post.downvoted_users.all():
            # User is changing their vote from downvote to upvote
            post.downvoted_users.remove(request.user)
            post.upvoted_users.add(request.user)
            post.downvotes -= 1
            post.upvotes += 1
        else:
            # User is adding a new upvote
            post.upvoted_users.add(request.user)
            post.upvotes += 1
        post.save()
        return JsonResponse({"upvotes": post.upvotes, "downvotes": post.downvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def downvote_post(request, pk):
    if request.is_ajax() and request.method == "POST":
        post = get_object_or_404(Post, pk=pk)
        post.downvotes += 1
        post.save()
        return JsonResponse({"downvotes": post.downvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def upvote_comment(request, post_pk, comment_pk):
    if request.is_ajax() and request.method == "POST":
        comment = get_object_or_404(Comment, pk=comment_pk)
        comment.upvotes += 1
        comment.save()
        return JsonResponse({"upvotes": comment.upvotes})
    else:
        return JsonResponse({"error": "Invalid request"}, status=400)

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

#main_app/

@login_required
def add_photo(request, post_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        # Initialize the S3 client
        s3 = boto3.client(
            's3'
            # aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            # aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

        try:
            bucket = os.getenv('S3_BUCKET')
            print("bucket", os.getenv("S3_BASE_URL"))
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.getenv('S3_BASE_URL')}{bucket}/{key}"
            Photo.objects.create(url=url, post_id=post_id)
        except Exception as e:
            print(f'An error occurred uploading file to S3: {e}')
            # Consider using Django's logging framework or sending this error to an admin email

    return redirect('post_detail', post_id=post_id)

# def post_detail(request, post_id):
#     post = get_object_or_404(Post, pk=post_id)
#     photos = Photo.objects.filter(post=post)  # Retrieve all photos associated with the post
#     return render(request, 'post_detail.html', {'post': post, 'photos': photos})




# def post_detail(request, post_id):
#     post = get_object_or_404(Post, id = post_id)
#     comments = post.comments.all()
    
#     if request.method == 'POST':
#         # Handle POST request to submit a new comment
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             new_comment = comment_form.save(commit=False)
#             new_comment.post = post
#             new_comment.author = request.user  # Assign the authenticated user as the author
#             new_comment.save()
#     else:
#         # Handle GET request (render the comment form)
#         comment_form = CommentForm()
    
#     return render(request, 'main_app/post_detail.html', {'post': post, 'comments': comments, 'comment_form': comment_form})
