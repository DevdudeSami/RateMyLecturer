from django.db import models
from django.contrib.auth.models import User

class University(models.Model):
    name = models.CharField(max_length=60, unique=True)

class Lecturer(models.Model):
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    university = models.ForeignKey(University)
    department = models.CharField(max_length=50)

    added_by = models.ForeignKey(User)

    class Meta:
        unique_together = ('first_name','last_name','university','department')

class Rating(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)

class Comment(models.Model):
    comment_text = models.TextField()
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)
