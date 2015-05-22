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
	timereq = models.IntegerField()
	startlat = models.DecimalField(max_digits=15, decimal_places=12)
	endlat = models.DecimalField(max_digits=15, decimal_places=12)
	startlong = models.DecimalField(max_digits=15, decimal_places=12)
	endlong = models.DecimalField(max_digits=15, decimal_places=12)
	minlat = models.DecimalField(max_digits=15, decimal_places=12)
	maxlat = models.DecimalField(max_digits=15, decimal_places=12)
	minlong = models.DecimalField(max_digits=15, decimal_places=12)
	maxlong = models.DecimalField(max_digits=15, decimal_places=12)