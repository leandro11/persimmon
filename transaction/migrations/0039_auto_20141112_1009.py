# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0038_auto_20141111_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionorder',
            name='transaction_claim',
            field=models.OneToOneField(related_name=b'order', verbose_name='\u8d34\u73b0\u7533\u8bf7', to='transaction.TransactionClaim'),
        ),
    ]
