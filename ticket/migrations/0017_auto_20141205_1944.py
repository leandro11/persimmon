# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0016_auto_20141204_0012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionticket',
            name='conductor',
        ),
        migrations.RemoveField(
            model_name='transactionticket',
            name='director',
        ),
        migrations.AlterField(
            model_name='ticketlog',
            name='after_status',
            field=models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'CHECKIN_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'CHECKIN', '\u5165\u5e93\u5df2\u6838'), (b'CHECKOUT_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'CHECKOUT', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
        migrations.AlterField(
            model_name='ticketlog',
            name='before_status',
            field=models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'CHECKIN_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'CHECKIN', '\u5165\u5e93\u5df2\u6838'), (b'CHECKOUT_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'CHECKOUT', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='status',
            field=models.CharField(default=b'RECEIVED_PENDING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5b8c\u6210'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5b8c\u6210'), (b'CHECKIN_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'CHECKIN', '\u5165\u5e93\u5b8c\u6210'), (b'CHECKOUT_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'CHECKOUT', '\u51fa\u5e93\u5b8c\u6210')]),
        ),
    ]
