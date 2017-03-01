from django.conf.urls import url
from . import views
from . import requests

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^login/', views.user_login, name='login'),
    url(r'^logout/', views.user_logout, name='logout'),

    # requests
    url(r'^requests/checkUsernameExists$', requests.checkUsernameExists, name='requests_checkUsernameExists'),
]
