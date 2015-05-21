# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0004_auto_20150521_1040'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='routeendlats',
        ),
        migrations.RemoveField(
            model_name='route',
            name='routeendlongs',
        ),
        migrations.RemoveField(
            model_name='route',
            name='routestartlats',
        ),
        migrations.RemoveField(
            model_name='route',
            name='routestartlongs',
        ),
        migrations.AddField(
            model_name='route',
            name='lats',
            field=models.TextField(default='123'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='longs',
            field=models.TextField(default='123'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='maxlat',
            field=models.CharField(default='123', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='maxlong',
            field=models.CharField(default='123', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='minlat',
            field=models.CharField(default='123', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='minlong',
            field=models.CharField(default='123', max_length=250),
            preserve_default=False,
        ),
    ]
