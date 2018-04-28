# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from core import update_status

# Create your models here.

class Profile(models.Model):
	auth_method=models.CharField(max_length=200)
	oauth_user_id=models.CharField(max_length=200, null=True)
	user=models.OneToOneField(User)
	

class Group(models.Model):
	company_name=models.CharField(max_length=200)



class Account(models.Model):
	user=models.ForeignKey(User)
	access_token=models.CharField(max_length=200)
	account_name=models.CharField(max_length=200,null=True, blank=True)
	thumbnail=models.URLField(null=True, blank=True)
	account_type=models.CharField(max_length=200, null=True, blank=True)
	other_info=models.CharField(max_length=200, null=True, blank=True)
	access_token_secret=models.CharField(max_length=200, null=True, blank=True)
	oauth_id=models.CharField(max_length=200, null=True)
	group=models.ForeignKey(Group, null=True, blank=True)

	def __str__(self):
		return self.account_name + ' ' + self.account_type



class Post(models.Model):
	content=models.TextField()
	account=models.ManyToManyField(Account)
	user=models.ForeignKey(User)
	scheduling_type=models.CharField(max_length=200, choices=(('Schedule Manually', 'Schedule Manually'),
		(settings.APPNAME+' Queue',settings.APPNAME+' Queue'),('Post Now','Post Now')))
	time_slot=models.DateTimeField(null=True, blank=True)
	status=models.CharField(max_length=200)

	def set_time_slot(self):
		#TODO work on this to support other scheduling method
		if self.scheduling_type=='Post Now':
			self.time_slot=timezone.now()
		if self.scheduling_type==settings.APPNAME+' Queue':
			add_pt()	
			

	def set_user_status(self, request):
		self.user=request.user
		self.status='Queing'


	def publish_post(self, account_object):
		update_status(self, account_object)
		self.status='Published'
		self.save()


		

class PostImage(models.Model):
	image=models.ImageField()
	post=models.ForeignKey(Post)



class Day(models.Model):
	day_name=models.CharField(max_length=20)
	day_no=models.IntegerField()

	def __str__(self):
		return self.day_name

class Timeslot(models.Model):
	time=models.TimeField()
	day=models.ForeignKey(Day)
	account=models.ForeignKey(Account)
	status=models.BooleanField(default=True)# to check if timeslot has been used, True means it has not been used


	def is_available(self):
		return self.status

class PublishingTime(models.Model):
	post=models.ForeignKey(Post)
	account=models.ForeignKey(Account)
	datetime=models.DateTimeField()
	status=models.BooleanField(default=False)
	timeslot=models.ForeignKey(Timeslot, null=True, blank=True)

	def publish(self):
		'''
		This function calls publish function for the post
		attached to self,
		and free the timeslot too,
		so that it can be used by other post
		'''
		self.post.publish_post(self.account)
		self.status=True
		self.timeslot.status=True #timeslot freed
		self.timeslot.save()
		self.save()





#def add_pt() :
	''' 
	This function is suppose to handle the creation of post 
	publishing time for each account attached to teh post
	'''













