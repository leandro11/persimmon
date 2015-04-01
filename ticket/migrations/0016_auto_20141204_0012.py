# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0015_auto_20141204_0009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionticket',
            name='number',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u6c47\u7968\u53f7'),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='send_ems',
            field=models.CharField(max_length=50, null=True, verbose_name='\u51fa\u7968\u5feb\u9012', blank=True),
        ),
    ]
