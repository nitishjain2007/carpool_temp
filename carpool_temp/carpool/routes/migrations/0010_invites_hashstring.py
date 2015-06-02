# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0009_auto_20150601_0750'),
    ]

    operations = [
        migrations.AddField(
            model_name='invites',
            name='hashstring',
            field=models.CharField(default='123', max_length=255),
            preserve_default=False,
        ),
    ]
