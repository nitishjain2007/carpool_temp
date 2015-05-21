# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pools',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start', models.CharField(max_length=250)),
                ('end', models.CharField(max_length=250)),
                ('time', models.TimeField()),
                ('date', models.DateField()),
                ('routeid', models.IntegerField()),
                ('user', models.ForeignKey(to='login.Carusers')),
            ],
        ),
    ]
