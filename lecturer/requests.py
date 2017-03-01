from .models import University, Lecturer, Rating, Comment, Department
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.db.models import Q

INV_REQ = "invalidRequest5987@@!#inv_req"

@login_required
def searchUniversities(request):
    if request.method == 'POST':
        searchTerm = request.POST['searchTerm']

        universities = University.objects.filter(Q(name__startswith=searchTerm) | Q(short_name__startswith=searchTerm))

        result = ""
        template = loader.get_template('lecturer/universityResult.html')

        for university in universities:
            result += template.render({'university': university}, request)

        if result == "":
            result = "<p>No universities found.</p>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)

@login_required
def searchDepartments(request):
    if request.method == 'POST':
        university = University.objects.get(name=request.POST['university'])
        searchTerm = request.POST['searchTerm']

        departments = Department.objects.filter(name__startswith=searchTerm, university=university)

        result = ""
        template = loader.get_template('lecturer/departmentResult.html')

        for department in departments:
            result += template.render({'department': department}, request)

        if result == "":
            result = "<p>No departments found.</p>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)

def searchLecturers(request):
    if request.method == 'POST':
        searchTerm = request.POST['searchTerm']

        lecturers = Lecturer.objects.filter(Q(first_name__startswith=searchTerm) | Q(last_name__startswith=searchTerm))

        result = ""
        template = loader.get_template('lecturer/lecturerResult.html')

        for lecturer in lecturers:
            result += template.render({'lecturer': lecturer}, request)

        if result == "":
            result = "<p>No lecturers found.</p>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)

@login_required
def rateLecturer(request):
    if request.method == 'POST':
        lecturer = Lecturer.objects.get(pk=request.POST['lecturerID'])
        value = request.POST['value']

        rating = Rating.objects.filter(user=request.user, lecturer=lecturer)
        if rating.exists():
            rating = rating[0]
            rating.value = value
        else:
            rating = Rating(value=value, lecturer=lecturer, user=request.user)

        rating.save()

        return HttpResponse('')

    return HttpResponse(INV_REQ)

@login_required
def getRatingForLecturer(request):
    if request.method == 'POST':
        lecturer = Lecturer.objects.get(pk=request.POST['lecturerID'])

        rating = Rating.objects.filter(user=request.user, lecturer=lecturer)
        if rating.exists():
            return HttpResponse(rating[0].value)
        return HttpResponse("NONE")

    return HttpResponse(INV_REQ)

def getAverageRating(request):
    if request.method == 'POST':
        lecturer = Lecturer.objects.get(pk=request.POST['lecturerID'])

        return HttpResponse(lecturer.get_rating())

    return HttpResponse(INV_REQ)
