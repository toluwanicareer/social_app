import tweepy
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
import datetime

def update_status(post_object, account_object):
	files=[item.image.file for item in post_object.postimage_set.all()]
	media_ids=[]
	api=get_tweet_api(account_object)
	for file in files:
		res=api.media_upload(file)
		media_ids.append(res.media_id)
	api.update_status(status=post_object.content, media_ids=media_ids)
		


def get_tweet_api(account_object):
	auth=tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
	auth.set_access_token(account_object.token.access_token, account_object.token.access_token_secret)
	return tweepy.API(auth)




def get_request_token(request,callback_url='http://localhost:8000/twitter_login'):
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






def get_day_no_from_today():
	'''
	return the weekday
	@return: weekday number
	''' 
	today=timezone.now()
	return today.weekday()


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)