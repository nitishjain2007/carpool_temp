# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0007_auto_20150525_0621'),
    ]

    operations = [
        migrations.AddField(
            model_name='pools',
            name='route_reverse',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
