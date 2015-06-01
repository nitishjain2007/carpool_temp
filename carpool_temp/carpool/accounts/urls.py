from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login.as_view(), name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register.as_view(), name='register'),
    url(r'^home/', views.home, name='home'),
    url(r'^authenticateuser/', views.authenticateuser.as_view(), name='authenticateuser'),
    url(r'^twitter_login/', views.twitter_login.as_view(), name='twitter_login'),
    url(r'^addmail/', views.addmail.as_view(), name='addmail'),
    url(r'^verifymail/(?P<secretstring>[-\w]+)/', views.verifymail.as_view(), name='verifymail'),
    url(r'^checkifvalidmail/(?P<email>[-\w]+)/', views.checkifvalidmail, name='checkifvalidmail'),
    url(r'^updateinfo/', views.updateinfo.as_view(), name='updateinfo'),
]