# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20150529_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='profile_pic',
            field=models.ImageField(upload_to=b'/images/profile_pics'),
        ),
    ]
