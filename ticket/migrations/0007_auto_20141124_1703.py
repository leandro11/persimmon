# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0006_auto_20141112_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='accountant',
            field=models.ForeignKey(related_name=b'invoice_accountant', verbose_name='\u5f00\u7968\u4f1a\u8ba1', blank=True, to='management.Staff', null=True),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='market_manager',
            field=models.ForeignKey(related_name=b'invoice_market_manager', verbose_name='\u5f00\u7968\u7ecf\u7406', to='management.Staff'),
        ),
    ]
