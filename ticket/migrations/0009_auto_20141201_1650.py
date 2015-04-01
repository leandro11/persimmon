# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0008_auto_20141201_1021'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transactionticket',
            name='ems',
        ),
        migrations.AddField(
            model_name='transactionticket',
            name='receive_ems',
            field=models.CharField(default='asf1', unique=True, max_length=50, verbose_name='\u5165\u7968\u5feb\u9012'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionticket',
            name='send_ems',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u51fa\u7968\u5feb\u9012', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='invoice',
            name='status',
            field=models.CharField(default=b'PROCESSING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5bc4\u51fa'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')]),
        ),
        migrations.AlterField(
            model_name='transactionticket',
            name='status',
            field=models.CharField(default=b'RECEIVED_PENDING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
    ]
