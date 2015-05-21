from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^signin/', views.signin, name='signin'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^authenticate/', views.authenticate, name='authenticate'),
    url(r'^signout/', views.signout, name='signout'),
    url(r'^createuser/', views.createuser, name='createuser'),
]