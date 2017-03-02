from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from lecturer.models import University

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')

    picture = models.ImageField(upload_to='profile_images', blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_active = models.DateTimeField(default=timezone.now)

    university = models.ForeignKey(University)

    def __str__(self):
        return self.user.username


def checkUserExists(username):
    return User.objects.filter(username=username).exists()
