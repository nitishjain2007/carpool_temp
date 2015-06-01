''' THE CONTROLLER FOR ACCOUNTS '''

from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.views.generic import View
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.mail import send_mail, BadHeaderError
from .models import Verifications, Extendeduser
from .forms import Extendeduserform
import hashlib




##################################################################################################################################################################
####################################### THE APP CONTROLS ALL OF THE FUNCTIONS THAT DEAL WITH THE CRUD OF THE USER ACCOUNTS #######################################
##################################################################################################################################################################




#The class for login
class login(View):
	def get(self, request, *args, **kwargs):
		if request.user.is_anonymous():
			#user is not logged in.. redirect him to the login page for login
			return render(request, 'accounts/signin.html')
		else:
			#user is already logged in.. redirect him to his home page
			return redirect('/accounts/home')




#The class for retrieving email of the user(twitter only)
class twitter_login(View):
	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		#check if the user has already given his email address
		if request.user.email == '':
			#user has not provided the email.. ask for the same
			request.user.is_active = 0
			request.user.save()
			return render(request, 'accounts/addmail.html')
		else:
			#user has provided his email.. redirect him to his home page
			return redirect('/accounts/home')




#Class for adding the retrieved mail and verification process
class addmail(View):

	def createverification(self, request):
		#first append username, email, first name, last name and a dummy string..
		string = request.user.username + request.user.email + request.user.first_name + request.user.last_name + "verificationthisissecret"
		#take sha and md5
		secretstring = hashlib.sha512(string.encode('utf-8')).hexdigest()
		supersecretstring = hashlib.md5(secretstring.encode('utf-8')).hexdigest()
		#create an instance for verification and save
		verification = Verifications(hashstring = supersecretstring, user = request.user)
		verification.save()
		return supersecretstring

	def sendmail(self, request, supersecretkey, email):
		#generate an url for the user and send the mail
		subject = "Verification of email account"
		url_required = "http://localhost:8000/accounts/verifymail/" + supersecretkey
		message = "Hi " + request.user.first_name + "\nPlease verify your email account by going to the following link: \n" + url_required
		send_mail(subject, message, "contact@spa.com", [email])

	def post(self, request, *args, **kwargs):
		email = request.POST.get("email", "")
		#saving of the email of the user in the database
		request.user.email = email
		request.user.save()
		#create a verification code and obtain the supersecretkey.. 
		supersecretkey = self.createverification(request)
		#send the verification mail..
		self.sendmail(request, supersecretkey, email)
		return HttpResponse("Please check your inbox and verify your mail...!!!")





#Class for updating the user's 'extendeduser' data
class updateinfo(View):
	def createnewrecord(self, request, extendeduser):
		#create a new entry for the user and save the records..
		extendeduser = Extendeduser.objects.get(user=request.user)
		extendeduser.profile_pic = request.FILES['file']
		extendeduser.mobile_no = request.POST.get("phone", "")
		extendeduser.address = request.POST.get("adress", "")
		extendeduser.save()

	def updaterecord(self, request):
		#update the existing records for the user..
		extendeduserinstance = Extendeduser(profile_pic=request.FILES['file'], user=request.user, mobile_no=request.POST.get("phone", ""), address=request.POST.get("adress", ""))
		extendeduserinstance.save()

	@method_decorator(login_required)
	#form is posted
	def post(self, request, *args, **kwargs):
		form = Extendeduserform(request.POST, request.FILES)
		if form.is_valid():
			#find if the entry for the user alreay exists..
			try:
				extendeduser = Extendeduser.objects.get(user=request.user)
				#on success update
				self.createnewrecord(request, extendeduser)
				return redirect('/accounts/home')        		
			except Extendeduser.DoesNotExist:
				#on failure create a new record
				self.updaterecord(request)
				return redirect('/accounts/home')

	@method_decorator(login_required)
	#called initially, display page with the form
	def get(self, request, *args, **kwargs):
		form = Extendeduserform()
		return render(request, 'accounts/upload.html', {'form': form})





#Class for activating the user after he hits the url sent to him on mail..
class verifymail(View):
	def get(self, request, *args, **kwargs):
		#get the user who is requesting verification from Verifications model
		requiredfield = Verifications.objects.get(hashstring = self.kwargs['secretstring'])
		user = requiredfield.user
		#activate the user
		user.is_active = 1
		user.save()
		return HttpResponse("Your account is verified, please login now....!!!!!")




def checkifvalidmail(request, email = None):
	try:
		results = User.objects.get(email=email)
	except User.DoesNotExist:
		return HttpResponse("Ok")
	return HttpResponse("Email id taken")




#Class for authenticating Users after filling up the login form
class authenticateuser(View):
	def post(self, request, *args, **kwargs):
		email = request.POST.get("email", "")
		password = request.POST.get("password", "")
		redirecturl = request.POST.get("redirecturl", "")
		#check if the credentials provided are authentic or not
		user = authenticate(username = email, password = password)
		#authentication successfull
		if user is not None:
			auth_login(request, user)
			if redirecturl == "":
				return redirect('/accounts/home')
			else:
				return redirect(redirecturl)
		#authentication failed
		else:
			return redirect('/accounts/login')




#function for logging out the user
def logout(request):
	auth_logout(request)
	return redirect('/accounts/login')




#Class for registering a user and generating verifications for the same..
class register(View):

	def createuser(self, request):
		email = request.POST.get("email", "")
		first_name = request.POST.get("first_name", "")
		last_name = request.POST.get("last_name", "")
		password = request.POST.get("password", "")
		user = User.objects.create_user(email, email, password)
		user.first_name = first_name
		user.last_name = last_name
		#user is not active.. activated upon email verification
		user.is_active = 0
		user.save()
		return user

	def createverification(self, request, user):
		#create a verification through different encryption combinations(sha + md5) and save them
		string = user.username + user.email + user.first_name + user.last_name + "verificationthisissecret"
		secretstring = hashlib.sha512(string.encode('utf-8')).hexdigest()
		supersecretstring = hashlib.md5(secretstring.encode('utf-8')).hexdigest()
		verification = Verifications(hashstring = supersecretstring, user = user)
		verification.save()
		return supersecretstring

	def sendverificationmail(self, request, user, supersecretstring):
		#create a verification mail and send it to the user..
		subject = "Verification of email account"
		url_required = "http://localhost:8000/accounts/verifymail/" + supersecretstring
		message = "Hi " + user.first_name + "\nPlease verify your email account by going to the following link: \n" + url_required
		send_mail(subject, message, "contact@spa.com", [request.POST.get("email", "")])

	#The initial page.. return the simple page with register form
	def get(self, request, *args, **kwargs):
		return render(request, 'accounts/register.html')

	#user fills up the registration form.. 
	def post(self, request, *args, **kwargs):
		#create an instance of the user and save it
		user = self.createuser(request)
		#create a verification for the user
		supersecretstring = self.createverification(request, user)
		#send user a verification mail on his mail id
		self.sendverificationmail(request, user, supersecretstring)
		return HttpResponse("Please check your inbox and verify your mail...!!!")	

	

@login_required
#the home page for the user..
def home(request):
	context = {'user': request.user}
	return render(request, 'accounts/home.html', context)