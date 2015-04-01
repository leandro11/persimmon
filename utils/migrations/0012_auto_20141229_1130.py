# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0011_auto_20141226_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
    ]
