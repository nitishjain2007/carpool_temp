from django.db import models
from login.models import Carusers

# Create your models here.
class Pools(models.Model):
	time = models.TimeField()
	date = models.DateField()
	routeid = models.IntegerField()
	user = models.ForeignKey(Carusers)

class Route(models.Model):
	lats = models.TextField()
	longs = models.TextField()
	startlat = models.CharField(max_length=250)
	endlat = models.CharField(max_length=250)
	startlong = models.CharField(max_length=250)
	endlong = models.CharField(max_length=250)
	minlat = models.CharField(max_length=250)
	maxlat = models.CharField(max_length=250)
	minlong = models.CharField(max_length=250)
	maxlong = models.CharField(max_length=250)