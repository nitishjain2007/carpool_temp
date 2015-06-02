from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^postride/', views.postride, name='postride'),
    url(r'^getride/', views.getride, name='getride'),
    url(r'^createride/', views.createride.as_view(), name='createride'),
    url(r'^retrieveride/(?P<page_id>[0-9]+)/', views.retrieveride, name='retrieveride'),
    url(r'^retrieveride/', views.retrieveride.as_view(), name='retrieveride'),
    url(r'^retrieverequiredrides/', views.retrieverequiredrides, name='retrieverequiredrides'),
    url(r'^makerequestride/', views.makerequestride, name='makerequestride'),
    url(r'^sendinvitetopool/', views.sendinvitetopool, name='sendinvitetopool'),
    url(r'^makerequestride/', views.makerequestride, name='makerequestride'),
]