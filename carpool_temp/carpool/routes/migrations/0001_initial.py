# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Pools',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('route_reverse', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lats', models.TextField()),
                ('longs', models.TextField()),
                ('timereq', models.IntegerField()),
                ('startlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('endlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('startlong', models.DecimalField(max_digits=15, decimal_places=12)),
                ('endlong', models.DecimalField(max_digits=15, decimal_places=12)),
                ('minlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('maxlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('minlong', models.DecimalField(max_digits=15, decimal_places=12)),
                ('maxlong', models.DecimalField(max_digits=15, decimal_places=12)),
            ],
        ),
        migrations.AddField(
            model_name='pools',
            name='route',
            field=models.ForeignKey(to='routes.Route'),
        ),
        migrations.AddField(
            model_name='pools',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
