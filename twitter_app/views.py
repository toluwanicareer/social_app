# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from login_app.models import Profile,Account
from login_app.views import update_or_create_account
from django.conf import settings
import tweepy
from twitter_core import get_tweet_auth, get_request_token
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
import pdb

# Create your views here.


class TwitterLoginMixin:
	account_type=settings.TWITTER_ACCOUNT_NAME
	user=None
	def get(self,request, *args, **kwargs):
		
		
		if request.GET.get('oauth_verifier'):
			
			verifier= request.GET.get('oauth_verifier')
			auth=get_tweet_auth(request,verifier)
			api = tweepy.API(auth)
			tw_user=api.me()
			#pdb.set_trace()
			if not self.user:

				try:
					profile=Profile.objects.get(oauth_user_id=tw_user.id)
					self.user=profile.user
				except Profile.DoesNotExist:
					user=User.objects.create(username=self.user_prefix+tw_user.screen_name+user_suffix, is_active=True)
					user.save()
					Profile.objects.create(auth_method=settings.account_type, user=user, oauth_user_id=tw_user.id).save()
					self.user=user
			if self.user :
				
				exist=update_or_create_account(tw_user.id, access_token=auth.access_token,
				secret=auth.access_token_secret , request=request, 
				tw_user=tw_user, account_type=self.account_type, user=self.user)	
				if not request.user.is_authenticated():

					login(request,self.user)
				return HttpResponseRedirect(reverse(self.after_login_url))
			



				
				

		'''
		handle login
		'''
		if request.is_ajax():

			response=get_request_token(request,self.redirect_url)
		return JsonResponse(response)



class loginTwitter(TwitterLoginMixin, View):
	after_login_url=settings.AFTER_LOGIN_URL
	user_prefix='TW__'
	user_suffix=''
	redirect_url=settings.TWITTER_LOGIN_URL
	
	

class add_twitter_account(TwitterLoginMixin, View):
	#Remember to put loginrequired Mixin here
	redirect_url=settings.TWITTER_ADD_ACCOUNT_URL
	
	after_login_url=settings.AFTER_LOGIN_URL


	def get(self,request, *args, **kwargs):
		self.user=request.user
		return super(add_twitter_account,self).get(request, *args, **kwargs)
		
	