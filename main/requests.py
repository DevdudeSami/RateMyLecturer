from lecturer.models import University
from django.http import HttpResponse

INV_REQ = "invalidRequest5987@@!#inv_req"

def getAllUniversitiesAsOptions(request):
    if request.method == 'POST':
        universities = University.objects.all()

        result = "<option value=\"NONE\">Select university...</option>"
        for university in universities:
            result += "<option value=\""+str(university.id)+"\""+">"+university.name+"</option>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)
