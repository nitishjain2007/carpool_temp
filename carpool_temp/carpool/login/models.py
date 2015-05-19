from django.db import models

# Create your models here.
class Carusers(models.Model):
	name = models.CharField(max_length=200)
	email_id = models.EmailField(max_length=254)
	password = models.CharField(max_length=200)
