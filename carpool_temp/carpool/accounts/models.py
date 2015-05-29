from django.db import models
from django.contrib.auth.models import User
from carpool.settings import MEDIA_ROOT

# Create your models here.

class Extendeduser(models.Model):
	profile_pic = models.ImageField(upload_to= MEDIA_ROOT + "/images/profile_pics")
	mobile_no = models.CharField(max_length=255)
	address = models.TextField()
	user = models.ForeignKey(User)

class Verifications(models.Model):
	hashstring = models.CharField(max_length=255)
	user = models.ForeignKey(User)