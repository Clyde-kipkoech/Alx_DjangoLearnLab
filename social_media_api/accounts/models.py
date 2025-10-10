from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    # Followers: users who follow this user
    # Following: users that this user follows (reverse of related_name)
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def follow(self, user):
        """Follow another user."""
        self.following.add(user)

    def unfollow(self, user):
        """Unfollow another user."""
        self.following.remove(user)

    def is_following(self, user):
        """Check if this user is following another user."""
        return self.following.filter(id=user.id).exists()

    def followers_count(self):
        """Return number of followers."""
        return self.followers.count()

    def following_count(self):
        """Return number of users this user is following."""
        return self.following.count()

    def __str__(self):
        return self.username
