import tweepy
from django.conf import settings

def update_twitter_status(post_object, account_object):
	files=[item.image.file for item in post_object.postimage_set.all()]
	media_ids=[]
	api=get_tweet_api(account_object)
	for file in files:
		res=api.media_upload(file)
		media_ids.append(res.media_id)
	api.update_status(status=post_object.content, media_ids=media_ids)
		


def get_tweet_api(account_object):
	auth=tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET)
	auth.set_access_token(account_object.access_token_info.access_token, account_object.access_token_info.access_token_secret)
	return tweepy.API(auth)




def get_request_token(request,callback_url=settings.TWITTER_LOGIN_URL):
	context=dict()
	auth = tweepy.OAuthHandler(settings.TWITTER_KEY, settings.TWITTER_SECRET, callback_url)
	try:
		redirect_url = auth.get_authorization_url()
		request.session['request_token']=auth.request_token
		context['redirect']=True
		context['redirect_url']=redirect_url
		return context
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