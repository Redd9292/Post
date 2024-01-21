from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Define the function here
def get_default_user_id():
    User = get_user_model()
    user, created = User.objects.get_or_create(username='default_user')
    return user.id

class Subpost(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)  # NEW CHANGES!!!
    downvote = models.IntegerField(default=0) #NEW CHANGES !!!
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
    
class Photo(models.Model):
    url = models.CharField(max_length=200)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for post_id: {self.post_id} @{self.url}"

    # Many-to-many fields for tracking votes
    upvoted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_posts', blank=True)
    downvoted_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_posts', blank=True)

    @property
    def upvotes(self):
        return self.upvoted_users.count()

    @property
    def downvotes(self):
        return self.downvoted_users.count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)

    def __str__(self):
        return self.text


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subpost = models.ForeignKey(Subpost, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} subscribed to {self.subpost.name}"
    
    def promote_to_moderator(self):
        self.is_moderator = True
        self.save()
    

