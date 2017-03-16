from django.shortcuts import render
from lecturer.models import Lecturer, University

def index(request):
    lecturers = reversed(sorted(Lecturer.objects.all(), key=lambda r: r.get_rating())[-5:])
    universities = reversed(sorted(University.objects.all(), key=lambda r: r.get_rating())[-5:])

    return render(request, 'main/index.html', {'lecturers': lecturers, 'universities': universities})
