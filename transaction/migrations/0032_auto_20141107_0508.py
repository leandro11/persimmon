# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0031_auto_20141107_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionoperation',
            name='remark',
            field=models.CharField(max_length=200, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
    ]
