from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from lecturer.models import University, Comment, CommentScore

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')

    picture = models.ImageField(upload_to='profile_images', blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)

    university = models.ForeignKey(University)

    def __str__(self):
        return self.user.username

    def score(self):
        total = 0

        # Get all comments by user
        comments = Comment.objects.filter(user=self.user)
        # For each comment, get score and add to total
        for comment in comments:
            total += comment.score()

        return total

def checkUserExists(username):
    return User.objects.filter(username=username).exists()
