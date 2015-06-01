# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('routes', '0008_pools_route_reverse'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invites',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_from_driver', models.BooleanField()),
                ('pool', models.ForeignKey(to='routes.Pools')),
            ],
        ),
        migrations.CreateModel(
            name='Riderequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('startlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('endlat', models.DecimalField(max_digits=15, decimal_places=12)),
                ('startlong', models.DecimalField(max_digits=15, decimal_places=12)),
                ('endlong', models.DecimalField(max_digits=15, decimal_places=12)),
                ('accepted', models.BooleanField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='invites',
            name='riderequest',
            field=models.ForeignKey(to='routes.Riderequest'),
        ),
    ]
