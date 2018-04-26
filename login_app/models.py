# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
	scheduling_type=models.CharField(max_length=200, choices=(('Schedule Manually', 'Schedule Mnaually'),
		(settings.APPNAME+' Scheduling',settings.APPNAME+' Scheduling'),('Post Now','Post Now')))
	time_slot=models.DateTimeField()
	status=models.CharField(max_length=200)

class PostImage(models.Model):
	image=models.ImageField()
	post=models.ForeignKey(Post)





