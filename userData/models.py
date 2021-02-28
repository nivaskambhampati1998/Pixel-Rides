from django.db import models
from django.contrib.auth.models import User

class UserDetailsInfo(models.Model):
	username = models.CharField(blank=False,max_length=50,default='')
	mPin = models.IntegerField(blank=False)
	isDriver = models.BooleanField(blank=True,default=False)

	def __str__(self):
		return self.username

class CloseContacts(models.Model):
	username = models.CharField(blank=False,max_length=50,default='')
	cc1 = models.CharField(blank=True,max_length=50,default='')
	cc2 = models.CharField(blank=True,max_length=50,default='')
	cc3 = models.CharField(blank=True,max_length=50,default='')
	cc4 = models.CharField(blank=True,max_length=50,default='')
	cc5 = models.CharField(blank=True,max_length=50,default='')

	def __str__(self):
		return self.username


class WalletMapping(models.Model):
	name = models.CharField(blank=False,max_length=50,default='')
	password = models.CharField(blank=True,max_length=100,default='',null=True)
	public = models.CharField(blank=True,max_length=500,default='',null=True)
	private = models.CharField(blank=True,max_length=500,default='',null=True)

	def __str__(self):
		return self.name

class WalletHistory(models.Model):
	sender = models.CharField(blank=False,max_length=50,default='')
	receiver = models.CharField(blank=True,max_length=50,default='',null=True)
	amount = models.IntegerField(blank=True,null=True)
	date = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return self.sender

class Scheduled_Rides(models.Model):
	username = models.CharField(blank=False,max_length=50,default='')
	source = models.CharField(blank=False,max_length=50, default='')
	destination = models.CharField(blank=False,max_length=50,default='')
	dateTime = models.DateTimeField(blank=True,null=True)

	def __str__(self):
		return self.username