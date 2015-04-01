# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0037_auto_20141229_2311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankattachment',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='enterpriseattachment',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
    ]
