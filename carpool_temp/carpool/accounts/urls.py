from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^register/', views.register, name='register'),
    url(r'^home/', views.home, name='home'),
    url(r'^authenticateuser/', views.authenticateuser, name='authenticateuser'),
    url(r'^registeruser/', views.registeruser, name='registeruser'),
    url(r'^send_email/', views.send_email, name='send_email'),
    url(r'^twitter_login/', views.twitter_login, name='twitter_login'),
    url(r'^addmail/', views.addmail, name='addmail'),
    url(r'^verifymail/(?P<secretstring>[-\w]+)/', views.verifymail, name='verifymail'),
    url(r'^checkifvalidmail/(?P<email>[-\w]+)/', views.checkifvalidmail, name='checkifvalidmail'),
    url(r'^updateinfo/', views.updateinfo, name='updateinfo'),
    url(r'^writeinfo/', views.writeinfo, name='writeinfo'),
]