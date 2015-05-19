from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Carusers

# Create your views here.

def index(request):
	template = loader.get_template('login/index.html')
	if 'email_id' not in request.session:
		username = "not in"
	else:
		username = request.session['email_id']
	#return HttpResponse(template.render())
	return HttpResponse(username)

def signin(request):
	if 'email_id' in request.session:
		del request.session['email_id']
	template = loader.get_template('login/signin.html')
	return render(request, 'signin.html')

def signup(request):
	template = loader.get_template('login/signup.html')
	return HttpResponse(template.render())

def authenticate(request):
	email_id = request.POST.get("email_id", "")
	password = request.POST.get("password", "")
	p = get_object_or_404(Carusers, email_id=email_id)
	request.session['email_id'] = email_id
	return HttpResponseRedirect(reverse('login:index'))
