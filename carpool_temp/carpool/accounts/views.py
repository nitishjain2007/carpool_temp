from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
	return render(request, 'accounts/signin.html')

def authenticateuser(request):
	email = request.POST.get("email", "")
	password = request.POST.get("password", "")
	user = authenticate(username = email, password = password)
	if user is not None:
		auth_login(request, user)
		return redirect('/accounts/home')
	else:
		return redirect('/accounts/login')

def logout(request):
	auth_logout(request)
	return redirect('/accounts/login')

def register(request):
	return render(request, 'accounts/register.html')

def registeruser(request):
	email = request.POST.get("email", "")
	first_name = request.POST.get("first_name", "")
	last_name = request.POST.get("last_name", "")
	password = request.POST.get("password", "")
	user = User.objects.create_user(email, email, password)
	user.first_name = first_name
	user.last_name = last_name
	user.is_active = False
	user.save()
	user = authenticate(username = email, password = password)
	auth_login(request, user)
	return redirect('/accounts/home')

@login_required
def home(request):
	context = {'user': request.user}
	return render(request, 'accounts/home.html', context)