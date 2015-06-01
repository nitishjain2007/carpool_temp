''' THE CONTROLLER FOR THE POOLS AND ROUTES '''
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.views.generic import View
from django.core.cache import cache
from .models import Pools, Route
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
import socket
import hashlib
import datetime




##################################################################################################################################################################
################################### THE APP CONTROLS ALL OF THE FUNCTIONS THAT DEAL WITH THE CRUD OF THE USER POOLS AND RIDES ####################################
##################################################################################################################################################################



#the global variable for storing the lat longs if the user chooses to refresh the page...
latlongs = []


#the function for displaying the initial page for posting a carpool
@login_required
def postride(request):
	return render(request, 'routes/postride.html')

@login_required
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
		return HttpResponse(type(startlat))


#the function for displaying the initial page for searching a carpool
@login_required
def getride(request):
	return render(request, 'routes/getride.html')

#this function displays the data through ajax .load function in pagenation
@login_required
@ensure_csrf_cookie
def retrieverequiredrides(request):
	#get the page id that has been requested
	page_id = int(request.GET.get("page", ""))
	print page_id
	ridereq = cache.get('recentridesearched')
	cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*3 + 3]
	context = {'results': cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*3 + 3]}
	return render(request, 'routes/displayrequiredroutes.html', context)

@login_required
def retrieveride(request,page_id=1):
	#get the ip address of the user (used for caching the user data for avoiding multiple database hits)
	ip = [(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
	if "startlat" in request.POST:
		keystring = ip + request.POST.get("startlat", "") + request.POST.get("startlong", "") + request.POST.get("endlat", "") + request.POST.get("endlong", "") + request.POST.get("date", "") + request.POST.get("time", "")[:4] + "ridesearch"
		keystring_hash = hashlib.md5(keystring.encode('utf-8')).hexdigest()
		if cache.get(keystring_hash) is None:
			print "cache is being created for " + keystring_hash
			startlat = float(request.POST.get("startlat", ""))
			startlong = float(request.POST.get("startlong", ""))
			endlat = float(request.POST.get("endlat", ""))
			endlong = float(request.POST.get("endlong", ""))
			global latlongs
			latlongs = []
			latlongs.append(startlat)
			latlongs.append(startlong)
			latlongs.append(endlat)
			latlongs.append(endlong)
			km = float(request.POST.get("km", ""))
			dates = request.POST.get("date", "")
			dates = dates.split(", ")
			time = request.POST.get("time", "")
			time = datetime.datetime.strptime(time, '%H:%M').time()
			for date in dates:
				datereq = date[:6] + date[8:]
				datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
			q1 = Route.objects.filter(minlat__lte = startlat + (0.005*km), maxlat__gte = startlat - (0.005*km), minlong__lte = startlong + (0.005*km), maxlong__gte = startlong - (0.005*km))
			q2 = q1.filter(minlat__lte = endlat + (0.005*km), maxlat__gte = endlat - (0.005*km), minlong__lte = endlong + (0.005*km), maxlong__gte = endlong - (0.005*km))
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
				longmatchstart1 = [ n for n,i in enumerate(longsf) if i>startlong - (0.005*km) ]
				longmatchstart2 = [ n for n,i in enumerate(longsf) if i<startlong + (0.005*km) ]
				latmatchstart1 = [ n for n,i in enumerate(latsf) if i>startlat - (0.005*km) ]
				latmatchstart2 = [ n for n,i in enumerate(latsf) if i<startlat + (0.005*km) ]
				startmatch = set(longmatchstart1)&set(longmatchstart2)&set(latmatchstart1)&set(latmatchstart2)
				startmatch = list(startmatch)
				longmatchend1 = [ n for n,i in enumerate(longsf) if i>endlong - (0.005*km) ]
				longmatchend2 = [ n for n,i in enumerate(longsf) if i<endlong + (0.005*km) ]
				latmatchend1 = [ n for n,i in enumerate(latsf) if i>endlat - (0.005*km) ]
				latmatchend2 = [ n for n,i in enumerate(latsf) if i<endlat + (0.005*km) ]
				endmatch = set(longmatchend1)&set(longmatchend2)&set(latmatchend1)&set(latmatchend2)
				endmatch = list(endmatch)
				if(len(startmatch) and len(endmatch)):
					routes.append(objects)
					routeids.append(objects.id)
					startmatchlist.append(startmatch)
					endmatchlist.append(endmatch)
			try:
				results = Pools.objects.filter(route__in = routes)
			except Pools.DoesNotExist:
				results = []
			finalresult = []
			dummyhalfhour = datetime.timedelta(seconds=1800)
			for i in range(len(results)):
				indexinmatches = routeids.index(results[i].route.id)
				if(results[i].route_reverse):
					if(startmatchlist[indexinmatches][0] >= endmatchlist[indexinmatches][0]):
						finalresult.append(results[i])
				else:
					if(startmatchlist[indexinmatches][0] <= endmatchlist[indexinmatches][0]):
						finalresult.append(results[i])
			finalresult1 = []
			for objects in finalresult:
				timereq = objects.route.timereq
				timereq = datetime.timedelta(seconds=timereq)
				if datereq == objects.date:
					if time >= (datetime.datetime.combine(datetime.date(1,1,1),time) - dummyhalfhour).time() and \
					time <= (datetime.datetime.combine(datetime.date(1,1,1),time) + timereq + dummyhalfhour).time():
						objects.route.timereq = objects.route.timereq/60
						finalresult1.append(objects)
			cache.set(keystring_hash, finalresult1, 3600)
			cache.set('recentridesearched', keystring_hash, 3600)
		else:
			cache.set('recentridesearched', keystring_hash, 3600)
			print "cache is being used for " + keystring_hash
	page_id = int(page_id)
	ridereq = cache.get('recentridesearched')
	global latlongs
	print latlongs
	if len(cache.get(ridereq)) % 3 == 0:
		pages = len(cache.get(ridereq))/3
	else:
		pages = len(cache.get(ridereq))/3 + 1
	context = {'results': cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*1 + 3], 'pagerange': [x+1 for x in range(0,pages)], 'current': page_id, 'userdata': latlongs}
	return render(request, 'routes/showrides.html', context)