from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from functools import reduce

class University(models.Model):
    name = models.CharField(max_length=60, unique=True)
    short_name = models.CharField(max_length=30, null=True)
    domain = models.CharField(max_length=30)

    def get_rating(self):
        lecturers = Lecturer.objects.filter(university=self)
        if not lecturers.exists(): return 0

        total = reduce((lambda x,y: x+y), map(lambda r: r.get_rating(), lecturers))
        return float(format(total/lecturers.count(), '.2f'))

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=60)
    university = models.ForeignKey(University)

    class Meta:
        unique_together = ('name', 'university')

    def __str__(self):
        return self.name + " in " + self.university.name

    def get_lecturers(self):
        return Lecturer.objects.filter(department=self)

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
        ratings = Rating.objects.filter(lecturer=self)
        if not ratings.exists(): return 0

        total = reduce((lambda x,y: x+y), map(lambda r: r.value, ratings))
        return float(format(total/ratings.count(), '.2f'))


class Rating(models.Model):
    value = models.IntegerField(default=0)
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)
    date_rated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Rating by " + self.user.username + " on " + self.lecturer.__str__()

    class Meta:
        unique_together = ('user', 'lecturer')

class Comment(models.Model):
    comment_text = models.TextField()
    user = models.ForeignKey(User)
    lecturer = models.ForeignKey(Lecturer)
    date_commented = models.DateTimeField(auto_now=True)
    is_anonymous = models.IntegerField(default=0)

    def __str__(self):
        return "Comment by " + self.user.username + " on " + self.lecturer.__str__()

    def score(self):
        scores = CommentScore.objects.filter(comment=self)

        if scores.exists():
            total = reduce((lambda x,y: x+y), map(lambda r: r.value, scores))
            return total
        else:
            return 0

    def getUserScore(self, user_id):
        # Returns 1 for up, 0 for none or -1 for down
        user = User.objects.get(pk=user_id)
        if user.id in CommentScore.objects.filter(comment=self).values_list('user', flat=True):
            return 1 if (CommentScore.objects.get(comment=self, user=user).value == 1) else -1
        else:
            return 0

    class Meta:
        unique_together = ('user', 'lecturer')

class CommentScore(models.Model):
    value = models.IntegerField()
    user = models.ForeignKey(User)
    comment = models.ForeignKey(Comment)
    date_scored = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ("Up" if (self.value == 1) else "Down") + " score, by " + self.user.username + " on " + self.comment.comment_text
