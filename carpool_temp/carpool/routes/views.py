from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from django.core.urlresolvers import reverse
from login.models import Carusers
from .models import Pools, Route
import datetime
# Create your views here.
def postride(request):
	return render(request, 'routes/postride.html')

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
	user = Carusers.objects.get(email_id = request.session['email_id'])
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

def getride(request):
	return render(request, 'routes/getride.html')

def retrieveride(request):
	startlat = float(request.POST.get("startlat", ""))
	startlong = float(request.POST.get("startlong", ""))
	endlat = float(request.POST.get("endlat", ""))
	endlong = float(request.POST.get("endlong", ""))
	dates = request.POST.get("date", "")
	dates = dates.split(", ")
	time = request.POST.get("time", "")
	time = datetime.datetime.strptime(time, '%H:%M').time()
	for date in dates:
		datereq = date[:6] + date[8:]
		datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
	q1 = Route.objects.filter(minlat__lte = startlat + 0.005, maxlat__gte = startlat - 0.005, minlong__lte = startlong + 0.005, maxlong__gte = startlong - 0.005)
	q2 = q1.filter(minlat__lte = endlat + 0.005, maxlat__gte = endlat - 0.005, minlong__lte = endlong + 0.005, maxlong__gte = endlong - 0.005)
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
		longmatchstart1 = [ n for n,i in enumerate(longsf) if i>startlong - 0.005 ]
		longmatchstart2 = [ n for n,i in enumerate(longsf) if i<startlong + 0.005 ]
		latmatchstart1 = [ n for n,i in enumerate(latsf) if i>startlat - 0.005 ]
		latmatchstart2 = [ n for n,i in enumerate(latsf) if i<startlat + 0.005 ]
		startmatch = set(longmatchstart1)&set(longmatchstart2)&set(latmatchstart1)&set(latmatchstart2)
		startmatch = list(startmatch)
		longmatchend1 = [ n for n,i in enumerate(longsf) if i>endlong - 0.005 ]
		longmatchend2 = [ n for n,i in enumerate(longsf) if i<endlong + 0.005 ]
		latmatchend1 = [ n for n,i in enumerate(latsf) if i>endlat - 0.005 ]
		latmatchend2 = [ n for n,i in enumerate(latsf) if i<endlat + 0.005 ]
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
		print time
		print (datetime.datetime.combine(datetime.date(1,1,1),time) - timereq).time()
		print (datetime.datetime.combine(datetime.date(1,1,1),time) + timereq).time()
		print datereq
		print objects.date
		if datereq == objects.date:
			print "yes"
			if time >= (datetime.datetime.combine(datetime.date(1,1,1),time) - dummyhalfhour).time() and \
			time <= (datetime.datetime.combine(datetime.date(1,1,1),time) + timereq + dummyhalfhour).time():
				finalresult1.append(objects)
	context = {'results': finalresult1}
	return render(request, 'routes/showrides.html', context)