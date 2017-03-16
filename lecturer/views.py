from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from .models import Lecturer, University, Department, Comment

def lecturerPage(request, lecturer_id):
    lecturer = Lecturer.objects.get(pk=lecturer_id)

    if request.user.is_authenticated:
        # Get whether user is in the university or not
        userInUni = request.user.user_profile.university.name == lecturer.university.name

        # Get whether user has commented on the lecturer
        userCommented = Comment.objects.filter(user=request.user, lecturer=lecturer).exists()

        return render(request, 'lecturer/lecturerPage.html', {'lecturer': lecturer, 'userInUni': userInUni, 'userCommented': userCommented})
    else:
        return render(request, 'lecturer/lecturerPage.html', {'lecturer': lecturer})

def universityPage(request, university_id):
    university = University.objects.get(pk=university_id)

    lecturers = Lecturer.objects.filter(university=university)

    return render(request, 'lecturer/universityPage.html', {'university': university, 'lecturers': lecturers})

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
