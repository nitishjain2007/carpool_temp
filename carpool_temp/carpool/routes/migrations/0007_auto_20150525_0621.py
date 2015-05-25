# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0006_auto_20150522_0620'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pools',
            name='routeid',
        ),
        migrations.AddField(
            model_name='pools',
            name='route',
            field=models.ForeignKey(default='123', to='routes.Route'),
            preserve_default=False,
        ),
    ]
