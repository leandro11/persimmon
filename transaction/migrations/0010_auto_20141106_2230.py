# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0009_auto_20141106_2214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionmetaoperation',
            options={'ordering': ('sequence',), 'verbose_name': '\u8d34\u73b0\u6d41\u7a0b\u64cd\u4f5c\u6a21\u677f', 'verbose_name_plural': '\u8d34\u73b0\u6d41\u7a0b\u64cd\u4f5c\u6a21\u677f'},
        ),
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='file_type',
            field=models.CharField(default=b'NONE', max_length=30, verbose_name='\u6587\u4ef6\u540d\u79f0', choices=[(b'NONE', '\u65e0\u9644\u4ef6'), (b'EXECUTION_AGREEMENT', '\u6267\u884c\u534f\u8bae'), (b'ENTRUST_DECLARATION', '\u59d4\u6258\u58f0\u660e'), (b'BILL_TICKET', '\u6c47\u7968'), (b'INVOICE', '\u53d1\u7968')]),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='file_type',
            field=models.CharField(default=b'NONE', max_length=30, verbose_name='\u6587\u4ef6\u540d\u79f0', choices=[(b'NONE', '\u65e0\u9644\u4ef6'), (b'EXECUTION_AGREEMENT', '\u6267\u884c\u534f\u8bae'), (b'ENTRUST_DECLARATION', '\u59d4\u6258\u58f0\u660e'), (b'BILL_TICKET', '\u6c47\u7968'), (b'INVOICE', '\u53d1\u7968')]),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='name',
            field=models.CharField(default=b'CASHIN_5DAY', unique=True, max_length=20, verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', choices=[(b'CASHIN_2DAY', '\u4e24\u65e5\u8d34\u73b0'), (b'CASHIN_3DAY', '\u4e09\u65e5\u8d34\u73b0'), (b'CASHIN_5DAY', '\u4e94\u65e5\u8d34\u73b0'), (b'CASHIN_7DAY', '\u4e03\u65e5\u8d34\u73b0')]),
        ),
    ]
