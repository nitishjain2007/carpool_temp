from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from login.models import Carusers
from .models import Pools, Route
import datetime
# Create your views here.
def postride(request):
	return render(request, 'routes/postride.html')

def createride(request):
	startlat = request.POST.get("startlat", "")
	startlong = request.POST.get("startlong", "")
	endlat = request.POST.get("endlat", "")
	endlong = request.POST.get("endlong", "")
	minlat = request.POST.get("minlat", "")
	maxlat = request.POST.get("maxlat", "")
	minlong = request.POST.get("minlong", "")
	maxlong = request.POST.get("maxlong", "")
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
		p = Route.objects.get(startlat = startlat, endlat = endlat, startlong = startlong, endlong = endlong)
		routeid = p.id
	except Route.DoesNotExist:
		p = Route(lats = latstr, longs = longstr, startlat = startlat, endlat = endlat, startlong = startlong, endlong = endlong, minlat = minlat, maxlat = maxlat, minlong = minlong, maxlong = maxlong)
		p.save()
		routeid = p.id
	for date in dates:
		datereq = date[:6] + date[8:]
		datereq = datetime.datetime.strptime(datereq, '%m/%d/%y').date()
		q = Pools(time = time, date = datereq, routeid = routeid, user = user)
		q.save()
	return HttpResponse("Your rides created successfully :). Now wait :P")

def getride(request):
	return render(request, 'routes/getride.html')	