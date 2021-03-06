# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-29 11:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0011_auto_20180428_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_token', models.CharField(max_length=200)),
                ('access_token_secret', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='account',
            name='access_token_info',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login_app.Token'),
        ),
    ]
