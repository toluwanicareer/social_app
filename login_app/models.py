# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from .core import update_status, get_day_no_from_today, next_weekday
from django.db.models import Q
from datetime import  timedelta
import datetime
import pdb
# Create your models here.

class Profile(models.Model):
	auth_method=models.CharField(max_length=200)
	oauth_user_id=models.CharField(max_length=200, null=True)
	user=models.OneToOneField(User)
	

class Group(models.Model):
	company_name=models.CharField(max_length=200)


class AccountType(models.Model):
	name=models.CharField(max_length=200)

	def __str__(self):
		return self.name

class Token(models.Model):
	access_token=models.CharField(max_length=200)
	access_token_secret=models.CharField(max_length=200, null=True, blank=True)
	oauth_id=models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.oauth_id

class Account(models.Model):
	user=models.ForeignKey(User)
	
	account_name=models.CharField(max_length=200,null=True, blank=True)
	thumbnail=models.URLField(null=True, blank=True)
	account_type=models.ForeignKey(AccountType, null=True)
	other_info=models.CharField(max_length=200, null=True, blank=True)
	oauth_id=models.CharField(max_length=200, null=True)
	group=models.ForeignKey(Group, null=True, blank=True)
	access_token_info=models.ForeignKey(Token, null=True)

	def __str__(self):
		return self.account_name + ' ' 

	
	def save(self, *args, **kwargs):
		'''
		calls the generate timeslot function
		'''
		
		if not self.id:
			'''
			compatible with only python27
			'''
			super(Account, self).save(*args, **kwargs)
			self.generate_time_slot()	
			return True
		super(Account, self).save(*args, **kwargs)	
		

	def generate_time_slot(self,days=settings.TIMESLOT_DAYS , hrs=settings.TIMESLOT_HRS):
		'''
		create timeslot based on settings data
		'''
		days=Day.objects.filter(day_name__in=days)
		
		for day in days:
			for time in hrs :
				tm=Timeslot(time=datetime.time(time), account=self, day=day)
				tm.next_available_day =tm.calculate_next_available_date()
				tm.save()	

class Post(models.Model):
	content=models.TextField()
	account=models.ManyToManyField(Account)
	user=models.ForeignKey(User)
	scheduling_type=models.CharField(max_length=200, choices=(('Schedule Manually', 'Schedule Manually'),
		(settings.APPNAME+' Queue',settings.APPNAME+' Queue'),('Post Now','Post Now')))
	time_slot=models.DateTimeField(null=True, blank=True)
	status=models.CharField(max_length=200)
	total_publsihing_time=models.IntegerField(default=1)
	no_of_publsih_time=models.IntegerField(default=0)


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

	def publish_for_all_account(self):
		'''
		The function will pubilsh the content of the post for
		all account attached to the post
		'''
		accounts=self.account.all()
		for account in accounts:
			self.publish_post(account)


	def add_pt(self,account_object, publish_date=None) :
		''' 
		This function is suppose to handle the creation of post 
		publishing time for each account attached to the post
		'''
		if publish_date==None:
			try:
				next_slot=Timeslot.objects.available_slots(account_object)[0]
			except:
				#@TODO : this means that there is no timeslot assigned for that account at all
				#ways around, put a check to make sure that there is a timeslot for each account
				#and also set default timeslot for each account. 
				return False	
			if next_slot.has_expired:
				next_slot.next_available_day=next_slot.calculate_next_available_date()

			publish_date=next_slot.next_available_day
			#update the timeslot table to update the next available date
			next_slot.next_available_day=next_slot.calculate_next_available_date(next_slot.next_available_day)
			next_slot.save()
			#create the pt object
			pt=PublishingTime.objects.create(post=self,account=account_object,datetime=publish_date,timeslot=next_slot)
			pt.save()
	def save(self,form=None, *args, **kwargs):
		'''
		create publishing time for each account
		by calling @add_pt method for each account
		'''
		if not self.id: # check if post object already exist
			super(Post, self).save(*args, **kwargs)  # Call the "real" save() method.
			if form:
				form.save_m2m() 		
			if self.scheduling_type==settings.APPNAME+' Queue':
				self.schedule_post()



	def schedule_post(self):
		accounts=self.account.all()
		for account in accounts:
			self.add_pt(account)



class PostImage(models.Model):
	image=models.ImageField()
	post=models.ForeignKey(Post)



class Day(models.Model):
	day_name=models.CharField(max_length=20)
	day_no=models.IntegerField()

	
	class Meta:
		ordering=['day_no']

	def __str__(self):
		return self.day_name


class TimeslotQuerySet(models.QuerySet):
	def available_slots(self, account_object):
		return self.filter(Q(account=account_object), status=True).order_by('next_available_day')


class TimeslotManager(models.Manager):
	def get_queryset(self):
		return TimeslotQuerySet(self.model, using=self._db)  # Important!

	def available_slots(self, account_object):
		return self.get_queryset().available_slots(account_object)


class Timeslot(models.Model):
	time=models.TimeField()
	day=models.ForeignKey(Day)
	account=models.ForeignKey(Account)
	status=models.BooleanField(default=True)# to check if timeslot has been used, True means it has not been used
	objects=TimeslotManager()
	next_available_day=models.DateTimeField(null=True)#next available day
	last_used_date=models.DateTimeField(null=True)#the last time the slot was used

	def __str__(self):
		return self.day.day_name + ' ' +self.account.account_name

	def calculate_next_available_date(self,date=timezone.now()):
		
		#this function calculate the next available date that can
		#be used by the timeslot
		

		timeslot_weekday_no=self.day.day_no
		next_weekda=next_weekday(date, timeslot_weekday_no)
		return next_weekda


	def has_expired(self):
		'''checks if timeslot available time has expire, if 
		yes return True
		'''
		if not self.next_available_day 	or self.next_available_day < timezone.now():
			return True
   

	

class PublishingTime(models.Model):
	post=models.ForeignKey(Post)
	account=models.ForeignKey(Account)
	datetime=models.DateTimeField(blank=True, null=True)
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

	def delete(self, *args, **kwargs):
		'''
		Handle post delete
		Roll back last used date for the timeslot attached to it 
		'''
		ptdate=self.datetime
		
		qs=PublishingTime.objects.filter(Q(timeslot=self.timeslot), 
			Q(datetime__gt=self.datetime),
			Q(status=False),
			Q(datetime__gt=timezone.now())).order_by('datetime')
		for pt in qs:
			current_date=pt.datetime
			pt.datetime=ptdate
			pt.save()
			ptdate=current_date
		self.timeslot.next_available_day=ptdate	
		super(self,PublishingTime).delete(*args, **kwargs)








