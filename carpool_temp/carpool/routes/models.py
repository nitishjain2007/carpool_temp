from django.db import models
from login.models import Carusers

# Create your models here.
class Pools(models.Model):
	start = models.CharField(max_length=250)
	end = models.CharField(max_length=250)
	time = models.TimeField()
	date = models.DateField()
	routeid = models.IntegerField()
	user = models.ForeignKey(Carusers)

class Route(models.Model):
	startlat = models.CharField(max_length=250)
	endlat = models.CharField(max_length=250)
	startlong = models.CharField(max_length=250)
	endlong = models.CharField(max_length=250)
	routestartlats = models.TextField()
	routeendlats = models.TextField()
	routestartlongs = models.TextField()
	routeendlongs = models.TextField()