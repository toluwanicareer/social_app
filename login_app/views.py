# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views import View
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView,
                                  FormView)


import tweepy
from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.http import  HttpResponseRedirect
from django.core.urlresolvers import reverse
import pdb
from django.contrib.auth.models import User
from .models import Profile, Account
from django.contrib.auth import authenticate, login
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.contrib import messages
# Create your views here.


class LoginView(TemplateView):
	template_name='page-login.html'


class loginTwitter(View):
	def get(self,request, *args, **kwargs):
		

		if request.GET.get('oauth_verifier'):
			verifier= request.GET.get('oauth_verifier')
			auth=get_tweet_auth(request,verifier)
			api = tweepy.API(auth)
			tw_user=api.me()
			#pdb.set_trace()
			try:
				profile=Profile.objects.get(oauth_user_id=tw_user.id)
				user=profile.user
			except Profile.DoesNotExist:
				user=User.objects.create(username='TW__'+tw_user.screen_name, is_active=True)
				user.save()
				Profile.objects.create(auth_method='twitter', user=user, oauth_user_id=tw_user.id).save()
				user=User.objects.get(id=user.id)
				Account.objects.create(user=user,access_token=auth.access_token, access_token_secret=auth.access_token_secret, 
					account_name=tw_user.screen_name,account_type='twitter', thumbnail=tw_user.profile_image_url, oauth_id=tw_user.id
					)
			if user is not None:
				login(request, user)
			return HttpResponseRedirect(reverse('twitter:home'))

		'''
		handle login
		'''
		if request.is_ajax():
			response=get_request_token(request)
		return response



class add_twitter_account(View):
	
	def get(self,request, *args, **kwargs):
		if request.is_ajax():
			response=get_request_token(request,'http://localhost:8000/add_account/')
			return response

		if request.GET.get('oauth_verifier'):
			verifier= request.GET.get('oauth_verifier')
			auth=get_tweet_auth(request,verifier)
			api = tweepy.API(auth)
			tw_user=api.me()
			exist=update_or_create_account(tw_user.id, access_token=auth.access_token,secret=auth.access_token_secret , request=request, tw_user=tw_user)
			if not exist :
				messages.warning(request, 'Account creation not successful')
			else:
				messages.success(request,' Account added successfully')
			return HttpResponseRedirect(reverse('twitter:home'))


		





def update_or_create_account(oauth_id, **kwargs):
	#TODO rewrite this function using kwargs and args to fit a more generic model for other account
	request=kwargs['request']
	try:

		account=Account.objects.get(oauth_id=oauth_id)
		if account.user != request.user:
			#TODO :
		 	#Define different eroor code for each scenario and handle it properly
		 	#Account already exist error code
			return False
		has_change=account.access_token==kwargs['access_token']
		if not has_change:
			account.access_token=kwargs['access_token']
			account.access_token_secret=kwargs['secret']
			account.save()
		return True


	except Account.DoesNotExist:
		#TODO check if account exist for othe user
		
		user=request.user
		tw_user=kwargs['tw_user']
		Account.objects.create(user=user,access_token=kwargs['access_token'], access_token_secret=kwargs['secret'], 
					account_name=tw_user.screen_name,account_type='twitter', thumbnail=tw_user.profile_image_url, oauth_id=tw_user.id
					)
		return True

	except MultipleObjectsReturned:
		#TODO :
		 	#Define different eroor code for each scenario and handle it properly
		Account.objects.filter(oauth_id).delete()
		return False
















def get_request_token(request,callback_url='http://localhost:8000/'):
	context=dict()
	auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET, callback_url)
	try:
		redirect_url = auth.get_authorization_url()
		request.session['request_token']=auth.request_token
		context['redirect']=True
		context['redirect_url']=redirect_url
		return JsonResponse(context)
	except tweepy.TweepError:
		#TODO handle twitter error
		pass




def get_tweet_auth(request,verifier):
	auth=tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
	token=request.session['request_token']
	auth.request_token=token
	try:
		auth.get_access_token(verifier)
	except tweepy.TweepError:
		#TODO handle approval error
		pass
	auth.set_access_token(auth.access_token, auth.access_token_secret)
	return auth
