# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0048_auto_20141201_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionorder',
            name='invoice_status',
            field=models.CharField(default=b'UNLODGED', max_length=30, verbose_name='\u53d1\u7968\u72b6\u6001', choices=[(b'UNLODGED', '\u672a\u5f00\u5177'), (b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')]),
        ),
    ]
