# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0002_route'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='endlat',
        ),
        migrations.RemoveField(
            model_name='route',
            name='startlat',
        ),
    ]
