# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-02-16 15:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lecturer', '0003_auto_20170216_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lecturer',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lecturer.Department'),
        ),
    ]
