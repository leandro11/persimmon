# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0032_auto_20141107_0508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionoperation',
            name='transaction',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', blank=True, to='transaction.TransactionOrder', null=True),
        ),
    ]
