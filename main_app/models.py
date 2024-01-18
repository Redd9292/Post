from django.db import models
from django.contrib.auth.models import User

class Subpost(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    upvotes = models.IntegerField(default=0)  # NEW CHANGES!!!
    downvote = models.IntegerField(default=0) #NEW CHANGES !!!
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# class Post(models.Model):
#     title = models.CharField(max_length=250)
#     content = models.TextField()
#     author = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    # Add other fields as needed
    

    def __str__(self):
        return self.title


class Comment(models.Model): #NEW CHANGES
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)  # or use a ForeignKey to a User model
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


