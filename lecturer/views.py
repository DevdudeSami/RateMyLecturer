from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Lecturer, University

@login_required
def lecturerPage(request, lecturer_id):
    pass

@login_required
def searchForLecturer(request):
    pass

@login_required
def addLecturer(request):
    if request.method == 'POST':
        title = request.POST['title']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']
        print(request.POST)
        university = University.objects.get(name=request.POST['university'])
        department = request.POST['department']

        lecturer = Lecturer(title=title, first_name=firstName, last_name=lastName, university=university, department=department, added_by=request.user)
        lecturer.save()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'lecturer/addLecturer.html', {})
