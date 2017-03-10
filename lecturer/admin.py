from django.contrib import admin
from .models import University, Lecturer, Rating, Comment, Department, CommentScore

# Register your models here.
admin.site.register(University)
admin.site.register(Department)
admin.site.register(Lecturer)
admin.site.register(Rating)
admin.site.register(Comment)
admin.site.register(CommentScore)
