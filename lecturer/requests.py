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

        departments = Department.objects.filter(name__startswith=searchTerm)

        result = ""
        template = loader.get_template('lecturer/departmentResult.html')

        for department in departments:
            result += template.render({'department': department}, request)

        if result == "":
            result = "<p>No departments found.</p>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)
