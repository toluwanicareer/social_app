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
from .models import Profile, Account, PostImage, Token, AccountType
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.contrib import messages
# Create your views here.
from .forms import PostForm, ImagePostForm, PublishTimeForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone
#from .core import get_request_token,get_tweet_auth


class LoginView(View):
	template_name='page-login.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginView, self).dispatch(request, *args, **kwargs)

	def get(self, request, *args, **kwargs):
		postform=PostForm(request.user)
		#imageform=ImagePostForm()
		publishtimeform=PublishTimeForm()

		#pdb.set_trace()

		return render(request,  self.template_name, {'postform':postform,'ptform':PublishTimeForm })

	def post(self,request, *args, **kwargs):
		#upload then post
		#assign timeline
		if request.is_ajax():
			postform=PostForm(request.POST)

			if postform.is_valid():

				post=postform.save(commit=False)
				now = timezone.now()
				post.set_user_status(request)
				post.save(postform)
				if post.scheduling_type=='Schedule Manually':
					ptform=PublishTimeForm(request.POST)
					if ptform.is_valid():
						
						accounts=post.account.all()
						for account in accounts:
							ptobject=ptform.save(commit=False)
							ptobject.account=account
							ptobject.post=post
							ptobject.save()
					else:
						post.delete()
						messages.warning(request, ptform.errors)
						return JsonResponse({'status':True, 'url':reverse('login:home')})
				files=request.FILES.getlist('files[]')
				for file in files:
					PostImage(post=post, image=file).save()
				messages.success(request, 'Post Saved' )	
				#check scheduling type to know whether to publish now
				if post.scheduling_type=='Post Now':
					#try:
					post.publish_for_all_account()
					messages.success(request, 'Post Publisehd in accounts specified')
					#except:
					#messages.warning(request,'Network error could not make post now, so it has been scedules')
					#post.schedule_post()
			else:
				messages.warning(request, postform.errors)
			return JsonResponse({'status':True, 'url':reverse('login:home')})
		#for file in files:
		return HttpResponseRedirect(reverse('login:home'))
class Logout(View):

	def get(self, request, *args, **kwargs):
		logout(request)
		return HttpResponseRedirect(reverse('login:home'))

def update_or_create_account(oauth_id, **kwargs):
	#TODO rewrite this function using kwargs and args to fit a more generic model for other account
	request=kwargs['request']
	user=kwargs['user']
	try:

		account=Account.objects.get(oauth_id=oauth_id)
		
		if account.user != user:
			#TODO :
		 	#Define different eroor code for each scenario and handle it properly
		 	#Error : Account already exist error code for another user
			return False
		has_change=account.access_token_info.access_token==kwargs['access_token']
		if not has_change:
			account.access_token=kwargs['access_token']
			account.access_token_secret=kwargs['secret']
			account.save()
		return True


	except Account.DoesNotExist:
		
		tw_user=kwargs['tw_user']
		try:
			account_type=AccountType.objects.get(name__icontains=kwargs['account_type'])
		except AccountType.DoesNotExist:
			#TODO
			#Handle error for invalid account creation
			return False
		token_info=Token(access_token=kwargs['access_token'],
			oauth_id=oauth_id,access_token_secret=kwargs['secret'])
		token_info.save()
				
		account=Account(user=user, 
					account_name=tw_user.screen_name,
					account_type=account_type,
					 thumbnail=tw_user.profile_image_url, 
					 oauth_id=oauth_id,
					 access_token_info=token_info
					)
		account.save()
		
		return True

	except MultipleObjectsReturned:
		#TODO :
		 	#Define different eroor code for each scenario and handle it properly
		 	#Error:Means that this multiple of this account exist.raise error
		Account.objects.filter(oauth_id).delete()
		return False
















