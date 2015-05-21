from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^postride/', views.postride, name='postride'),
    url(r'^getride/', views.getride, name='getride'),
    url(r'^createride/', views.createride, name='createride'),
]