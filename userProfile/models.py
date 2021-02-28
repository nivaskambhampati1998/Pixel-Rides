from django.db import models
from django.contrib.auth.models import User

class UserRides(models.Model):
	username = models.CharField(blank=False,max_length=50,default='')
	source = models.CharField(blank=False,max_length=50,default='')
	destination = models.CharField(blank=False,max_length=50,default='')
	dateTime = models.DateTimeField(blank=False,max_length=50)
	driverId = models.CharField(blank=True,max_length=50, default='')
	amount = models.IntegerField(default=0)
	customerAgreed = models.BooleanField(default=False)
	driverAgreed = models.BooleanField(default=False)
	bargain = models.TextField(default='')
	paymentMethod = models.CharField(blank=True,max_length=50)
	isDone = models.BooleanField(default=False)
	stops = models.TextField(default="")

	def __str__(self):
		return self.username

class UserProfile(models.Model):
	Username=models.CharField(max_length=10,blank=False,default='')
	EmailAddress=models.CharField(blank=False,max_length=50,default='')
	FirstName=models.CharField(max_length=30,blank=False,default='')
	LastName=models.CharField(max_length=30,blank=True,default='')
	Address=models.CharField(blank=True,max_length=50,default='')
	City=models.CharField(max_length=20,blank=True,default='')
	Country=models.CharField(max_length=15,default='',blank=True)
	PostalCode=models.CharField(max_length=10,blank=True,default='')
	ProfilePic=models.ImageField(blank=True)

	def __str__(self):
		return self.Username