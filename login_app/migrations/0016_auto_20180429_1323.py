# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-04-29 12:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_app', '0015_auto_20180429_1315'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='login_app.AccountType'),
        ),
    ]
