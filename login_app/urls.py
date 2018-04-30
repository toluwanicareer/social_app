from django.conf.urls import url
from . import views

app_name='login'

urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name='home'),
    #url(r'^twitter_login/$', views.loginTwitter.as_view(), name='twitter_login'),
    #url(r'^add_account$', views.add_twitter_account.as_view(), name='add_account'),
    url(r'^logout/$', views.Logout.as_view(), name='logout'),
    ]