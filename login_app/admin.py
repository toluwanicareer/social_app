# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Profile, Post, PostImage, Timeslot, Day

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(PostImage)
admin.site.register(Timeslot)
admin.site.register(Day)