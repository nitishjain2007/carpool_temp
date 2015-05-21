# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('routes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startlat', models.CharField(max_length=250)),
                ('endlat', models.CharField(max_length=250)),
                ('startlong', models.CharField(max_length=250)),
                ('endlong', models.CharField(max_length=250)),
                ('routestartlats', models.TextField()),
                ('routeendlats', models.TextField()),
                ('routestartlongs', models.TextField()),
                ('routeendlongs', models.TextField()),
            ],
        ),
    ]
