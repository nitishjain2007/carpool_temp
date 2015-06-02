''' THE CONTROLLER FOR THE POOLS AND ROUTES '''
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.cache import cache
from .models import Pools, Route, Riderequest, Invites
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator	
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.mail import send_mail, BadHeaderError
import socket
import hashlib
import datetime




##################################################################################################################################################################
################################### THE APP CONTROLS ALL OF THE FUNCTIONS THAT DEAL WITH THE CRUD OF THE USER POOLS AND RIDES ####################################
##################################################################################################################################################################



#the global variable for storing the lat longs if the user chooses to refresh the page...
#the global variable for checking if the user has requested that ride or not ( used in checking invitation )

#the function for displaying the initial page for posting a carpool
@login_required
def postride(request):
	return render(request, 'routes/postride.html')

class createride(View):

	def retrievedata(self, request):
		startlat = float(request.POST.get("startlat", ""))
		startlong = float(request.POST.get("startlong", ""))
		endlat = float(request.POST.get("endlat", ""))
		endlong = float(request.POST.get("endlong", ""))
		minlat = float(request.POST.get("minlat", ""))
		maxlat = float(request.POST.get("maxlat", ""))
		minlong = float(request.POST.get("minlong", ""))
		maxlong = float(request.POST.get("maxlong", ""))
		timereq = int(request.POST.get("timereq", ""))
		latstr = request.POST.get("latstr", "")
		latstr = latstr[1:]
		longstr = request.POST.get("longstr", "")
		longstr = longstr[1:]
		dates = request.POST.get("date", "")
		dates = dates.split(", ")
		time = request.POST.get("time", "")
		time = datetime.datetime.strptime(time, '%H:%M').time()
		user = request.user
		data = {'startlat': startlat, 'startlong': startlong, 'endlat': endlat, 'endlong': endlong, 'minlat': minlat, 'minlong': minlong, 'timereq': timereq, 'latstr': latstr, 'longstr': longstr, 'dates': dates, 'time': time, 'user': user}
		return data

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		#retrieve the data collected from post variables
		data = self.retrievedata(request)
		#check if there exists a route already to the route that has to be inserted
		try:
			p = Route.objects.get(endlat__range = (data['endlat'] - 0.0000000001, data['endlat'] + 0.0000000001), startlat__range = (data['startlat'] - 0.0000000001, data['startlat'] + 0.0000000001), endlong__range = (data['endlong'] - 0.0000000001, data['endlong'] + 0.0000000001), startlong__range = (data['startlong'] - 0.0000000001, data['startlong'] + 0.0000000001))
			#on success assign the route to the route object recieved
			route = p
			route_reverse = False
		except Route.DoesNotExist:
			try:
				#check if the route exists in reverse order
				#eg if your route is A->B, check if B->A exists
				p = Route.objects.get(startlat__range = (data['endlat'] - 0.0000000001, data['endlat'] + 0.0000000001), endlat__range = (data['startlat'] - 0.0000000001, data['startlat'] + 0.0000000001), startlong__range = (data['endlong'] - 0.0000000001, data['endlong'] + 0.0000000001), endlong__range = (data['startlong'] - 0.0000000001, data['startlong'] + 0.0000000001))
				route = p
				#mark the route as reversed
				route_reverse = True
			except Route.DoesNotExist:
				#if the route does not exist either in reversed or non reversed form, create the route
				p = Route(lats = data['latstr'], longs = data['longstr'], startlat = data['startlat'], endlat = data['endlat'], startlong = data['startlong'], endlong = data['endlong'], minlat = data['minlat'], maxlat = data['maxlat'], minlong = data['minlong'], maxlong = data['maxlong'], timereq = data['timereq'])
				p.save()
				routeid = p
				route_reverse = False
		for date in data['dates']:
			#for each of the date, create a carpool..
			datereq = date[:6] + date[8:]
			datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
			q = Pools(time = data['time'], date = datereq, route = p, user = data['user'], route_reverse = route_reverse)
			q.save()
		return HttpResponse(type(data['startlat']))


#the function for displaying the initial page for searching a carpool
@login_required
def getride(request):
	return render(request, 'routes/getride.html')

@login_required
def makerequestride(request):
	request.session['riderequest'] = True
	#riderequest = True
	return HttpResponse(request.session['riderequest'])

#this function displays the data through ajax .load function in pagenation
@login_required
@ensure_csrf_cookie
def retrieverequiredrides(request):
	#get the page id that has been requested
	page_id = int(request.GET.get("page", ""))
	print page_id
	ridereq = cache.get('recentridesearched')
	#get the required results only.. for now 3 per page..
	cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*3 + 3]
	context = {'results': cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*3 + 3], 'requestride': request.session['riderequest']}
	return render(request, 'routes/displayrequiredroutes.html', context)

#the function manages the requests that are sent to the users to join carpools ( either way )
#class managerequest(View):
#	def post(self, request, *args, **kwargs):

@login_required
def sendinvitetopool(request):
	poolid = int(request.GET.get("poolid", ""))
	pool = Pools.objects.get(id=poolid)
	pooluser = pool.user
	subject = "Pool Joining Request By " + request.user.first_name + " " + request.user.last_name
	message = "Hi " + pooluser.first_name + "\n" + request.user.first_name + " " + request.user.last_name + " has sent you a request to join your carpool..."
	send_mail(subject, message, "contact@spa.com", [pooluser.email])
	return HttpResponse("success")

class retrieveride(View):

	def getip(self, request):
		return [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

	def retrievedata(self, request):
		#handling the global variables for refresh conditions
		#these specify the lat longs of the user ( for the purpose of drawing the users route on the map)
		latlongs = []
		latlongs.append(float(request.POST.get("startlat", "")))
		latlongs.append(float(request.POST.get("startlong", "")))
		latlongs.append(float(request.POST.get("endlat", "")))
		latlongs.append(float(request.POST.get("endlong", "")))
		print latlongs
		request.session['latlongs'] = latlongs
		dates = request.POST.get("date", "")
		dates = dates.split(", ")
		time = request.POST.get("time", "")
		time = datetime.datetime.strptime(time, '%H:%M').time()
		for date in dates:
			datereq = date[:6] + date[8:]
			datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
		data = {'startlat': float(request.POST.get("startlat", "")), 'startlong': float(request.POST.get("startlong", "")), 'endlat': float(request.POST.get("endlat", "")), 'endlong': float(request.POST.get("endlong", "")), 'km': float(request.POST.get("km", "")), 'datereq': datereq, 'time': time}
		return data

	def filteronroute(self,request,data,q2):
		routes = []
		routeids = []
		startmatchlist = []
		endmatchlist = []
		for objects in q2:
			lats = objects.lats
			longs = objects.longs
			lats = lats.split(",")
			longs = longs.split(",")
			latsf = [float(i) for i in lats]
			longsf = [float(i) for i in longs]
			longmatchstart1 = [ n for n,i in enumerate(longsf) if i>data['startlong'] - (0.005*data['km']) ]
			longmatchstart2 = [ n for n,i in enumerate(longsf) if i<data['startlong'] + (0.005*data['km']) ]
			latmatchstart1 = [ n for n,i in enumerate(latsf) if i>data['startlat'] - (0.005*data['km']) ]
			latmatchstart2 = [ n for n,i in enumerate(latsf) if i<data['startlat'] + (0.005*data['km']) ]
			startmatch = set(longmatchstart1)&set(longmatchstart2)&set(latmatchstart1)&set(latmatchstart2)
			startmatch = list(startmatch)
			longmatchend1 = [ n for n,i in enumerate(longsf) if i>data['endlong'] - (0.005*data['km']) ]
			longmatchend2 = [ n for n,i in enumerate(longsf) if i<data['endlong'] + (0.005*data['km']) ]
			latmatchend1 = [ n for n,i in enumerate(latsf) if i>data['endlat'] - (0.005*data['km']) ]
			latmatchend2 = [ n for n,i in enumerate(latsf) if i<data['endlat'] + (0.005*data['km']) ]
			endmatch = set(longmatchend1)&set(longmatchend2)&set(latmatchend1)&set(latmatchend2)
			endmatch = list(endmatch)
			#on suceesful match, append the route to the lists
			if(len(startmatch) and len(endmatch)):
				routes.append(objects)
				routeids.append(objects.id)
				startmatchlist.append(startmatch)
				endmatchlist.append(endmatch)
		returndata =  {'routes': routes, 'routeids': routeids, 'startmatchlist': startmatchlist, 'endmatchlist': endmatchlist}		
		return returndata

	@method_decorator(login_required)
	def get(self, request, *args, **kwargs):
		ridereq = cache.get('recentridesearched')
		print ridereq
		if len(cache.get(ridereq)) % 3 == 0:
			pages = len(cache.get(ridereq))/3
		else:
			pages = len(cache.get(ridereq))/3 + 1
		context = {'results': cache.get(ridereq)[0:3], 'pagerange': [x+1 for x in range(0,pages)], 'current': 0, 'userdata': request.session['latlongs'], 'requestride': request.session['riderequest']}
		return render(request, 'routes/showrides.html', context)

	@method_decorator(login_required)
	def post(self, request, *args, **kwargs):
		request.session['riderequest'] = False
		#get the ip address of the user (used for caching the user data for avoiding multiple database hits)
		ip = self.getip(request)
		#generate a hashstring for using in caches ( for easier access )
		keystring = ip + request.POST.get("startlat", "") + request.POST.get("startlong", "") + request.POST.get("endlat", "") + request.POST.get("endlong", "") + request.POST.get("date", "") + request.POST.get("time", "")[:4] + "ridesearch"
		keystring_hash = hashlib.md5(keystring.encode('utf-8')).hexdigest()
		#check if the data is already present in the cache or not
		if cache.get(keystring_hash) is None:
			#generate the data and store it in cache...
			data = self.retrievedata(request)
			#filter the routes on the basis of the largest and smallest latlongs for the first order filtering
			#this specifies for the start point of the user
			q1 = Route.objects.filter(minlat__lte = data['startlat'] + (0.005*data['km']), maxlat__gte = data['startlat'] - (0.005*data['km']), minlong__lte = data['startlong'] + (0.005*data['km']), maxlong__gte = data['startlong'] - (0.005*data['km']))
			#this specifies for the end point of the user
			q2 = q1.filter(minlat__lte = data['endlat'] + (0.005*data['km']), maxlat__gte = data['endlat'] - (0.005*data['km']), minlong__lte = data['endlong'] + (0.005*data['km']), maxlong__gte = data['endlong'] - (0.005*data['km']))
			returndata = self.filteronroute(request,data,q2)
			routes = returndata['routes']
			routeids = returndata['routeids']
			startmatchlist = returndata['startmatchlist']
			endmatchlist = returndata['endmatchlist']
			#get the pools on the routes which match the user requirements
			try:
				results = Pools.objects.filter(route__in = routes)
			except Pools.DoesNotExist:
				results = []
			finalresult = []
			dummyhalfhour = datetime.timedelta(seconds=1800)
			for i in range(len(results)):
				indexinmatches = routeids.index(results[i].route.id)
				#check if the route recieved is stored as the reverse in the pool and act accordingly..
				if(results[i].route_reverse):
					#check if start point comes after end point (route reversed)
					if(startmatchlist[indexinmatches][0] >= endmatchlist[indexinmatches][0]):
						finalresult.append(results[i])
				else:
					#check if start point comes before end point (normal route)
					if(startmatchlist[indexinmatches][0] <= endmatchlist[indexinmatches][0]):
						finalresult.append(results[i])
			#check if the time suites the user
			finalresult1 = []
			for objects in finalresult:
				timereq = objects.route.timereq
				timereq = datetime.timedelta(seconds=timereq)
				if data['datereq'] == objects.date:
					if data['time'] >= (datetime.datetime.combine(datetime.date(1,1,1),data['time']) - dummyhalfhour).time() and \
					data['time'] <= (datetime.datetime.combine(datetime.date(1,1,1),data['time']) + timereq + dummyhalfhour).time():
						objects.route.timereq = objects.route.timereq/60
						finalresult1.append(objects)
			#cache the result for future purposes
			cache.set(keystring_hash, finalresult1, 3600)
			#set the current search as recent search
			cache.set('recentridesearched', keystring_hash, 3600)
		else:
			#set the current search as recent serach
			cache.set('recentridesearched', keystring_hash, 3600)
			print cache.get('recentridesearched')
		ridereq = cache.get('recentridesearched')
		if len(cache.get(ridereq)) % 3 == 0:
			pages = len(cache.get(ridereq))/3
		else:
			pages = len(cache.get(ridereq))/3 + 1
		context = {'results': cache.get(ridereq)[0:3], 'pagerange': [x+1 for x in range(0,pages)], 'current': 0, 'userdata': request.session['latlongs'], 'requestride': request.session['riderequest']}
		return render(request, 'routes/showrides.html', context)