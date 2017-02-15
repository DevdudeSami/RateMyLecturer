from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    date_joined = models.DateTimeField(default=timezone.now)
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username
    

def checkUserExists(username):
    return User.objects.filter(username=username).exists()
