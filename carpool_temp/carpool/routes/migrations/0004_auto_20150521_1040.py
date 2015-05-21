# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0003_auto_20150521_1027'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pools',
            name='end',
        ),
        migrations.RemoveField(
            model_name='pools',
            name='start',
        ),
        migrations.AddField(
            model_name='route',
            name='endlat',
            field=models.CharField(default='1111', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='route',
            name='startlat',
            field=models.CharField(default='123', max_length=250),
            preserve_default=False,
        ),
    ]
