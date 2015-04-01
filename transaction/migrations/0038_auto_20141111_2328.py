# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0037_transactionclaim_receivable_enterprise'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionoperation',
            name='operator_member_type',
            field=models.CharField(default='PLATFORM', max_length=30, verbose_name='\u6267\u884c\u65b9\u7c7b\u578b', choices=[('BANK', b'\xe9\x93\xb6\xe8\xa1\x8c\xe4\xbc\x9a\xe5\x91\x98'), ('ENTERPRISE', b'\xe4\xbc\x81\xe4\xb8\x9a\xe4\xbc\x9a\xe5\x91\x98'), ('PLATFORM', b'\xe6\x80\xa1\xe6\x99\xba\xe8\x9e\x8d\xe9\x80\x9a')]),
        ),
        migrations.AlterField(
            model_name='transactionorder',
            name='status',
            field=models.CharField(default=b'PROCESSING', max_length=20, verbose_name='\u8d34\u73b0\u8ba2\u5355\u72b6\u6001', choices=[(b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'DONE', '\u5df2\u5b8c\u6210'), (b'ABORT', '\u5df2\u4f5c\u5e9f')]),
        ),
    ]
