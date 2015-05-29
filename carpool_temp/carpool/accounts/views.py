from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail, BadHeaderError
from .models import Verifications, Extendeduser
from .forms import Extendeduserform
import hashlib

# Create your views here.
def login(request, path=None):
	if request.user.is_anonymous():
		return render(request, 'accounts/signin.html')
	else:
		return redirect('/accounts/home')

@login_required
def twitter_login(request):
	if request.user.email == '':
		request.user.is_active = 0
		request.user.save()
		return render(request, 'accounts/addmail.html')
	else:
		return redirect('/accounts/home')

@login_required
def addmail(request):
	email = request.POST.get("email", "")
	request.user.email = email
	request.user.save()
	string = request.user.username + request.user.email + request.user.first_name + request.user.last_name + "verificationthisissecret"
	secretstring = hashlib.sha512(string.encode('utf-8')).hexdigest()
	supersecretstring = hashlib.md5(secretstring.encode('utf-8')).hexdigest()
	verification = Verifications(hashstring = supersecretstring, user = request.user)
	verification.save()
	subject = "Verification of email account"
	url_required = "http://localhost:8000/accounts/verifymail/" + supersecretstring
	message = "Hi " + request.user.first_name + "\nPlease verify your email account by going to the following link: \n" + url_required
	send_mail(subject, message, "contact@spa.com", [email])
	#return render(request, '/accounts/verifymailpage.html')
	return HttpResponse("Please check your inbox and verify your mail...!!!")

@login_required
def updateinfo(request):
	form = Extendeduserform()
	return render(request, 'accounts/updateinfo.html', {'form': form})

def writeinfo(request):
	if request.method == 'POST':
		form = Extendeduserform(request.POST)
		if form.is_valid():
			print "hi"
			image = form.cleaned_data['image']
			phoneno = form.cleaned_data['phoneno']
			updateinfo = Extendeduser(profile_pic = image, mobile_no = phoneno)
			updateinfo.user = request.user
			updateinfo.save()
		else:
			print form.errors
	return HttpResponse("data added")

def verifymail(request, secretstring):
	requiredfield = Verifications.objects.get(hashstring = secretstring)
	user = requiredfield.user;
	user.is_active = 1
	user.save()
	return HttpResponse("Your account is verified, please login now....!!!!!")

def checkifvalidmail(request, email = None):
	print email
	try:
		results = User.objects.get(email=email)
	except User.DoesNotExist:
		return HttpResponse("Ok")
	return HttpResponse("Email id taken")

def send_email(request):
	subject = "Test Mail"
	message = "Hi this is a test mail... Please ignore"
	from_email = "Dont Reply <do_not_reply@domain.com>"
	if subject and message and from_email:
		try:
			send_mail(subject, message, from_email, ['spamailserver@gmail.com'])
		except BadHeaderError:
			return HttpResponse('Invalid header found.')
		return HttpResponseRedirect('/contact/thanks/')
	else:
		# In reality we'd use a form class
		# to get proper validation errors.
		return HttpResponse('Make sure all fields are entered and valid.')

def authenticateuser(request):
	email = request.POST.get("email", "")
	password = request.POST.get("password", "")
	redirecturl = request.POST.get("redirecturl", "")
	user = authenticate(username = email, password = password)
	if user is not None:
		auth_login(request, user)
		if redirecturl == "":
			return redirect('/accounts/home')
		else:
			return redirect(redirecturl)
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
	user.is_active = 0
	user.save()
	string = user.username + user.email + user.first_name + user.last_name + "verificationthisissecret"
	secretstring = hashlib.sha512(string.encode('utf-8')).hexdigest()
	supersecretstring = hashlib.md5(secretstring.encode('utf-8')).hexdigest()
	verification = Verifications(hashstring = supersecretstring, user = user)
	verification.save()
	subject = "Verification of email account"
	url_required = "http://localhost:8000/accounts/verifymail/" + supersecretstring
	message = "Hi " + user.first_name + "\n Please verify your email account by going to the following link: \n " + url_required
	send_mail(subject, message, "contact@spa.com", [email])
	return HttpResponse("Please check your inbox and verify your mail...!!!")	

@login_required
def home(request):
	context = {'user': request.user}
	return render(request, 'accounts/home.html', context)