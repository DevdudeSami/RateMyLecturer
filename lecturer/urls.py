from django.conf.urls import url
from . import views
from . import requests

urlpatterns = [
    url(r'^$', views.searchForLecturer, name='searchForLecturer'),
    url(r'^search$', views.searchForLecturer, name='searchForLecturer'),
    url(r'^add$', views.addLecturer, name='addLecturer'),
    url(r'^(?P<lecturer_id>[0-9]+)/$', views.lecturerPage, name='lecturerPage'),

    # requests
    url(r'^requests/searchUniversities$', requests.searchUniversities, name='searchUniversities'),
    url(r'^requests/searchDepartments$', requests.searchDepartments, name='searchDepartments'),
    url(r'^requests/searchLecturers$', requests.searchLecturers, name='searchLecturers'),

]
