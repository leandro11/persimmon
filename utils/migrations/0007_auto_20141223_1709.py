# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0006_auto_20141223_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='name',
            field=models.CharField(help_text='\u6240\u6709\u6a21\u677f\u6587\u6863\u6587\u4ef6\u540d\u4e0d\u53ef\u91cd\u590d', unique=True, max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
    ]
