# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.models import User
from login_app.models import Profile,Account, 

# Create your views here.


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
