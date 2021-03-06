# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-23 15:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lecturer', '0004_auto_20170216_1516'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentScore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('date_scored', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='date_commented',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='lecturer',
            name='date_added',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='rating',
            name='date_rated',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='university',
            name='domain',
            field=models.CharField(default=django.utils.timezone.now, max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commentscore',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.Comment'),
        ),
        migrations.AddField(
            model_name='commentscore',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
