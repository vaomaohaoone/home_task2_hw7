# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-08 22:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20170508_2228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scores',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 8, 22, 32, 28, 712437, tzinfo=utc)),
        ),
    ]