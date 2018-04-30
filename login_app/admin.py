# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, Post, PostImage, Timeslot, Day,PublishingTime, Token, Account, AccountType

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Timeslot)
admin.site.register(Day)
admin.site.register(PublishingTime)
admin.site.register(Token)
admin.site.register(Account)
admin.site.register(AccountType)