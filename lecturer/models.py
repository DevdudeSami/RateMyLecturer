from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class University(models.Model):
    name = models.CharField(max_length=60, unique=True)
    short_name = models.CharField(max_length=30, null=True)
    domain = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=60)
    university = models.ForeignKey(University)

    class Meta:
        unique_together = ('name', 'university')

    def __str__(self):
        return self.name + " in " + self.university.name

class Lecturer(models.Model):
    title = models.CharField(max_length=10)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_added = models.DateTimeField(default=timezone.now)

    university = models.ForeignKey(University)
    department = models.ForeignKey(Department)

    added_by = models.ForeignKey(User)

    class Meta:
        unique_together = ('first_name','last_name','university','department')

    def __str__(self):
        return self.title + " " + self.first_name + " " + self.last_name

    def get_rating(self):
        # Calculates the average rating
        ratings = Ratings.objects.filter(lecturer=self)
        total = reduce((lambda x,y: x+y), ratings)
        return total/ratings.count()


class Rating(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)
    date_rated = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Rating by " + self.user.username + " on " + self.lecturer

class Comment(models.Model):
    comment_text = models.TextField()
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)
    date_commented = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Comment by " + self.user.username + " on " + self.lecturer

class CommentScore(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    date_scored = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return "Score on comment: \n\n" + self.comment.comment_text + "\n\n by " + self.user.username
