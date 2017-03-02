from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Lecturer, University, Department

@login_required
def lecturerPage(request, lecturer_id):
    lecturer = Lecturer.objects.get(pk=lecturer_id)

    # Get whether user is in the university or not
    userInUni = request.user.user_profile.university.name == lecturer.university.name

    return render(request, 'lecturer/lecturerPage.html', {'lecturer': lecturer, 'userInUni': userInUni})

@login_required
def searchForLecturer(request):
    pass

@login_required
def addLecturer(request):
    if request.method == 'POST':
        title = request.POST['title']
        firstName = request.POST['firstName']
        lastName = request.POST['lastName']

        university = University.objects.get(name=request.POST['university'])
        department = Department.objects.get(name=request.POST['department'], university=university)

        lecturer = Lecturer(title=title, first_name=firstName, last_name=lastName, university=university, department=department, added_by=request.user)
        lecturer.save()

        return HttpResponseRedirect('/')
    else:
        return render(request, 'lecturer/addLecturer.html', {})
