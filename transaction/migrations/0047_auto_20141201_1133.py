# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0046_remove_transactionclaim_ticket_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionorder',
            name='invoice_status',
            field=models.CharField(default=b'UNLODGED', max_length=30, verbose_name='\u53d1\u7968\u72b6\u6001', choices=[(b'UNLODGED', '\u672a\u5f00\u5177'), (b'LODGED', '\u5df2\u7533\u8bf7'), (b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5b8c\u6210'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionorder',
            name='ticket_status',
            field=models.CharField(default=b'UNRECEIVED', max_length=30, verbose_name='\u6c47\u7968\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED', '\u5df2\u6536\u7968'), (b'VERIFIED', '\u5df2\u9a8c\u7968'), (b'ARRIVED', '\u5df2\u5165\u5e93'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u51fa\u5e93'), (b'ABORT', '\u5df2\u4f5c\u5e9f')]),
            preserve_default=True,
        ),
    ]
