from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from .models import Carusers

# Create your views here.

def index(request):
	if 'email_id' not in request.session:
		return HttpResponseRedirect(reverse('login:signin'))
	else:
		username = request.session['email_id']
	return render(request, 'login/index.html')

def signin(request):
	if 'email_id' in request.session:
		if(request.session['email_id'] is None):
			del request.session['email_id']
		else:
			return HttpResponseRedirect(reverse('login:index'))
	#template = loader.get_template('login/signin.html')
	return render(request, 'login/signin.html')

def signout(request):
	if 'email_id' in request.session:
		del request.session['email_id']
	return HttpResponseRedirect(reverse('login:signin'))

def signup(request):
	template = loader.get_template('login/signup.html')
	return render(request, 'login/signup.html')

def authenticate(request):
	email_id = request.POST.get("email_id", "")
	password = request.POST.get("password", "")
	try:
		p = Carusers.objects.get(email_id = email_id, password = password)
	except Carusers.DoesNotExist:
		p = None
	if p is not None:
		request.session['email_id'] = email_id
		request.session['name'] = p.name
		return HttpResponseRedirect(reverse('login:index'))
	else:
		request.session['email_id'] = None
		return HttpResponseRedirect(reverse('login:signin'))

def createuser(request):
	name = request.POST.get("name", "")
	email_id = request.POST.get("email_id", "")
	password = request.POST.get("password", "")
	q = Carusers(name = name, email_id = email_id, password = password)
	q.save()
	return HttpResponseRedirect(reverse('login:signin'))