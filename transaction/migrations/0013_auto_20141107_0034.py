# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0012_auto_20141107_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionorder',
            name='transaction_claim',
            field=models.OneToOneField(verbose_name='\u6536\u6b3e\u4f01\u4e1a', to='transaction.TransactionClaim'),
        ),
    ]
