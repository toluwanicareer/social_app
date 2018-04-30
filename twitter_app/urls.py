from django.conf.urls import url
from . import views

app_name='twitter'
urlpatterns = [
 url(r'^twitter_login/$', views.loginTwitter.as_view(), name='twitter_login'),
 url(r'^add_account$', views.add_twitter_account.as_view(), name='add_twitter_account'),
 ]