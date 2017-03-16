from django.conf.urls import url
from . import views, requests

urlpatterns = [
    url(r'^$', views.index, name='index'),

    # REQUESTS
    url(r'^requests/getAllUniversitiesAsOptions$', requests.getAllUniversitiesAsOptions, name='getAllUniversitiesAsOptions'),
]
