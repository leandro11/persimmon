# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0001_initial'),
        ('transaction', '0001_initial'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionticket',
            name='order',
            field=models.OneToOneField(verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='accountant',
            field=models.ForeignKey(related_name=b'accountant', verbose_name='\u5f00\u7968\u4f1a\u8ba1', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='market_manager',
            field=models.ForeignKey(related_name=b'market_manager', verbose_name='\u5f00\u7968\u7ecf\u7406', to='management.Staff'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='invoice',
            name='order',
            field=models.OneToOneField(verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
            preserve_default=True,
        ),
    ]
