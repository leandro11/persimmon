# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0047_auto_20141201_1133'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_rate_file',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='\u94f6\u884c\u8bc4\u7ea7\u626b\u63cf\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='upload_file',
            field=models.FileField(upload_to=b'.', null=True, verbose_name='\u9644\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='transactionorder',
            name='invoice_status',
            field=models.CharField(default=b'UNLODGED', max_length=30, verbose_name='\u53d1\u7968\u72b6\u6001', choices=[(b'UNLODGED', '\u672a\u5f00\u5177'), (b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5bc4\u51fa'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')]),
        ),
        migrations.AlterField(
            model_name='transactionorder',
            name='ticket_status',
            field=models.CharField(default=b'UNRECEIVED', max_length=30, verbose_name='\u6c47\u7968\u72b6\u6001', choices=[(b'UNRECEIVED', '\u672a\u6536\u7968'), (b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838'), (b'ABOR_PENDINGT', '\u4f5c\u5e9f\u5f85\u6838'), (b'ABORT', '\u4f5c\u5e9f\u5df2\u6838')]),
        ),
    ]
