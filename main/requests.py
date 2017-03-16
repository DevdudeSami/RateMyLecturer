from lecturer.models import University
from django.http import HttpResponse


def getAllUniversitiesAsOptions(request):
    if request.method == 'POST':
        universities = University.objects.all()

        result = ""
        for university in universities:
            result += "<option value=\""+str(university.id)+"\""+">"+university.name+"</option>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)
