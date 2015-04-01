# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0030_auto_20141107_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketformerholder',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u6301\u7968\u4eba\u540d\u79f0'),
        ),
    ]
