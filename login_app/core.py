import tweepy
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
import datetime
from twitter_app.twitter_core import update_twitter_status 


def update_status(post_object, account_object):
	if account_object.account_type.name=='twitter':
		update_twitter_status(post_object, account_object)


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


