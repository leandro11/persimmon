# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0013_auto_20141202_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoicelog',
            name='after_status',
            field=models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'UNLODGED', '\u672a\u5f00\u5177'), (b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')]),
        ),
        migrations.AlterField(
            model_name='invoicelog',
            name='before_status',
            field=models.CharField(default=b'UNLODGED', max_length=30, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'UNLODGED', '\u672a\u5f00\u5177'), (b'LODGED', '\u5df2\u5f00\u5177'), (b'FINISHED', '\u5df2\u5bc4\u51fa')]),
        ),
        migrations.AlterField(
            model_name='invoicelog',
            name='remarks',
            field=models.CharField(max_length=300, null=True, verbose_name='\u5907\u6ce8', blank=True),
        ),
        migrations.AlterField(
            model_name='ticketlog',
            name='after_status',
            field=models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
        migrations.AlterField(
            model_name='ticketlog',
            name='before_status',
            field=models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
        migrations.AlterField(
            model_name='ticketlog',
            name='ticket',
            field=models.ForeignKey(verbose_name='\u6c47\u7968', to='ticket.TransactionTicket'),
        ),
    ]
