# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-28 18:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0009_auto_20180428_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publishingtime',
            name='datetime',
            field=models.DateTimeField(null=True),
        ),
    ]
