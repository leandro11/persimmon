# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0004_auto_20141106_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='transaction',
            field=models.OneToOneField(related_name=b'invoice', verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='transaction',
            field=models.OneToOneField(related_name=b'ticket', verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
        ),
    ]
