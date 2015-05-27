from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Extendeduser(models.Model):
	profile_pic = models.CharField(max_length=255)
	mobile_no = models.CharField(max_length=255)
	address = models.TextField()
	user = models.ForeignKey(User)