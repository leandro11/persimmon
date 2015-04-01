# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0014_auto_20141202_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionticket',
            name='number',
            field=models.CharField(max_length=50, verbose_name='\u6c47\u7968\u53f7'),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='receive_ems',
            field=models.CharField(max_length=50, verbose_name='\u5165\u7968\u5feb\u9012'),
        ),
    ]
