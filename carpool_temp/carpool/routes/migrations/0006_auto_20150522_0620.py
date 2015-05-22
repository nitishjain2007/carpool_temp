# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0005_auto_20150521_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='route',
            name='timereq',
            field=models.IntegerField(default=123),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='route',
            name='endlat',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='endlong',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='maxlat',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='maxlong',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='minlat',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='minlong',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='startlat',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
        migrations.AlterField(
            model_name='route',
            name='startlong',
            field=models.DecimalField(max_digits=15, decimal_places=12),
        ),
    ]
