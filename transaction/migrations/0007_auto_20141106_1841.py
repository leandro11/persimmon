# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0006_transactionoperation_operate_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionorder',
            name='fee',
            field=models.DecimalField(default=1.1, verbose_name='\u670d\u52a1\u8d39  ', max_digits=10, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactionorder',
            name='amount',
            field=models.DecimalField(verbose_name='\u8d34\u73b0\u91d1\u989d', max_digits=11, decimal_places=2),
        ),
    ]
