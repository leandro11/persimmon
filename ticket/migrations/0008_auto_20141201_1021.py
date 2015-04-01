# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0007_auto_20141124_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default=b'PROCESSING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'LODGED', '\u5df2\u7533\u8bf7'), (b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5b8c\u6210'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')]),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='status',
            field=models.CharField(default=b'RECEIVED', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED', '\u5df2\u6536\u7968'), (b'VERIFIED', '\u5df2\u9a8c\u7968'), (b'ARRIVED', '\u5df2\u5165\u5e93'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u51fa\u5e93'), (b'ABORT', '\u5df2\u4f5c\u5e9f')]),
        ),
    ]
