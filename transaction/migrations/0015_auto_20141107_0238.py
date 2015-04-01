# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0014_auto_20141107_0154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionorder',
            name='transaction_claim',
            field=models.OneToOneField(verbose_name='\u8d34\u73b0\u7533\u8bf7', to='transaction.TransactionClaim'),
        ),
    ]
