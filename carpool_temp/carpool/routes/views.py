from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from django.core.cache import cache
from .models import Pools, Route
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import socket
import hashlib
import datetime
# Create your views here.

@login_required
def dummy(request):
	return HttpResponse(request.user)

@login_required
def postride(request):
	return render(request, 'routes/postride.html')

@login_required
def createride(request):
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
	try:
		p = Route.objects.get(endlat__range = (endlat - 0.0000000001, endlat + 0.0000000001), startlat__range = (startlat - 0.0000000001, startlat + 0.0000000001), endlong__range = (endlong - 0.0000000001, endlong + 0.0000000001), startlong__range = (startlong - 0.0000000001, startlong + 0.0000000001))
		route = p
		route_reverse = False
	except Route.DoesNotExist:
		try:
			p = Route.objects.get(startlat__range = (endlat - 0.0000000001, endlat + 0.0000000001), endlat__range = (startlat - 0.0000000001, startlat + 0.0000000001), startlong__range = (endlong - 0.0000000001, endlong + 0.0000000001), endlong__range = (startlong - 0.0000000001, startlong + 0.0000000001))
			route = p
			route_reverse = True
		except Route.DoesNotExist:
			p = Route(lats = latstr, longs = longstr, startlat = startlat, endlat = endlat, startlong = startlong, endlong = endlong, minlat = minlat, maxlat = maxlat, minlong = minlong, maxlong = maxlong, timereq = timereq)
			p.save()
			routeid = p
			route_reverse = False
	for date in dates:
		datereq = date[:6] + date[8:]
		datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
		q = Pools(time = time, date = datereq, route = p, user = user, route_reverse = route_reverse)
		q.save()
	return HttpResponse(type(startlat))

@login_required
def getride(request):
	return render(request, 'routes/getride.html')

@login_required
def retrieveride(request,page_id=1):
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
						finalresult1.append(objects)
			cache.set(keystring_hash, finalresult1, 3600)
			cache.set('recentridesearched', keystring_hash, 3600)
		else:
			cache.set('recentridesearched', keystring_hash, 3600)
			print "cache is being used for " + keystring_hash
	page_id = int(page_id)
	ridereq = cache.get('recentridesearched')
	if len(cache.get(ridereq)) % 3 == 0:
		pages = len(cache.get(ridereq))/3
	else:
		pages = len(cache.get(ridereq))/3 + 1
	context = {'results': cache.get(ridereq)[(page_id - 1)*3:(page_id - 1)*3 + 3], 'pagerange': [x+1 for x in range(0,pages)], 'current': page_id}
	return render(request, 'routes/showrides.html', context)