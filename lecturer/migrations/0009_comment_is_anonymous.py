# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-03 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lecturer', '0008_auto_20170303_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='is_anonymous',
            field=models.IntegerField(default=0),
        ),
    ]
