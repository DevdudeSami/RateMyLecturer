from .models import University, Lecturer, Rating, Comment, Department, CommentScore
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.db.models import Q
from django.utils import timezone

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
        if searchTerm == " ":
            lecturers = Lecturer.objects.all()

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

@login_required
def addComment(request):
    if request.method == 'POST':
        commentText = request.POST['commentText']
        lecturer = Lecturer.objects.get(pk=request.POST['lecturerID'])

        comment = Comment.objects.filter(user=request.user, lecturer=lecturer)
        if comment.exists():
            comment = comment[0]
            comment.comment_text = commentText
        else:
            comment = Comment(comment_text=commentText, user=request.user, lecturer=lecturer)

        if request.POST['isAnonymous'] == 'true':
            comment.is_anonymous = 1
        else:
            comment.is_anonymous = 0

        comment.save()

        return HttpResponse()

    return HttpResponse(INV_REQ)

def getComments(request):
    if request.method == 'POST':
        lecturer = Lecturer.objects.get(pk=request.POST['lecturerID'])

        comments = Comment.objects.filter(lecturer=lecturer).order_by('-date_commented')

        result = ""
        template = loader.get_template('lecturer/comment.html')

        for comment in comments:
            rating = Rating.objects.filter(user=comment.user, lecturer=comment.lecturer)

            context = {'comment': comment}
            
            if request.user.is_authenticated:
                context['userScore'] = comment.getUserScore(request.user.id)

            if rating.exists():
                context['rating'] = rating[0]

            result += template.render(context, request)

        if result == "":
            result = "<p>No comments on this lecturer. Please be the first.</p>"

        return HttpResponse(result)

    return HttpResponse(INV_REQ)

@login_required
def deleteComment(request):
    if request.method == 'POST':
        comment = Comment.objects.get(pk=request.POST['commentID'])
        comment.delete()

        return HttpResponse()

    return HttpResponse(INV_REQ)

@login_required
def changeScoreForComment(request):
    if request.method == 'POST':
        user = request.user
        comment = Comment.objects.get(pk=request.POST['comment_id'])
        value = request.POST['value']
        print(value)
        if value == "CLEAR":
            CommentScore.objects.get(user=user, comment=comment).delete()
            return HttpResponse("")

        if CommentScore.objects.filter(user=user, comment=comment).count() > 0:
            score = CommentScore.objects.get(user=user, comment=comment)
            score.value = value
            score.save()
        else:
            score = CommentScore(user=user, comment=comment, value=value)
            score.save()

        return HttpResponse("")
    else:
        return HttpResponse(INV_REQ)

def getDomainForUniversityName(request):
    if request.method == 'POST':
        name = request.POST['universityName']
        domain = University.objects.get(name=name).domain
        return HttpResponse(domain)
    else:
        return HttpResponse(INV_REQ)
