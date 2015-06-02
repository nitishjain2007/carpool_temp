from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Route(models.Model):
	lats = models.TextField()
	longs = models.TextField()
	timereq = models.IntegerField()
	startlat = models.DecimalField(max_digits=15, decimal_places=12)
	endlat = models.DecimalField(max_digits=15, decimal_places=12)
	startlong = models.DecimalField(max_digits=15, decimal_places=12)
	endlong = models.DecimalField(max_digits=15, decimal_places=12)
	minlat = models.DecimalField(max_digits=15, decimal_places=12)
	maxlat = models.DecimalField(max_digits=15, decimal_places=12)
	minlong = models.DecimalField(max_digits=15, decimal_places=12)
	maxlong = models.DecimalField(max_digits=15, decimal_places=12)

class Pools(models.Model):
	time = models.TimeField()
	date = models.DateField()
	route = models.ForeignKey(Route)
	route_reverse = models.BooleanField()
	user = models.ForeignKey(User)

class Riderequest(models.Model):
	time = models.TimeField()
	date = models.DateField()
	startlat = models.DecimalField(max_digits=15, decimal_places=12)
	endlat = models.DecimalField(max_digits=15, decimal_places=12)
	startlong = models.DecimalField(max_digits=15, decimal_places=12)
	endlong = models.DecimalField(max_digits=15, decimal_places=12)
	user = models.ForeignKey(User)
	accepted = models.BooleanField()

class Invites(models.Model):
	pool = models.ForeignKey(Pools)
	hashstring = models.CharField(max_length=255)
	riderequest = models.ForeignKey(Riderequest)
	is_from_driver = models.BooleanField()