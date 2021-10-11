from django.urls import include, path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'announcements/$', views.Announcements.as_view()),
    #url(r'registration/$', views.Registration.as_view()),
    #url(r'metro/$', views.Metros.as_view()),
    #url(r'city/$', views.Citys.as_view()),
]
