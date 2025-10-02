from django.db import models

# Create your models here.

from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    # add tags relationship (keep blank=True so existing posts are fine)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    
    def __str__(self):
        return self.title
    
class Profile(models.Model):   # <--- ADD THIS
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_pic = models.ImageField(upload_to="profile_pics", default="default.jpg")

    def __str__(self):
        return f"{self.user.username} Profile"
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']  # oldest first (change if you prefer newest first)

    def __str__(self):
        return f'Comment by {self.author.username} on "{self.post.title}"'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name