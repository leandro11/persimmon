# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0050_auto_20141205_1944'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='operator_member',
            field=models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'PAYER', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'TICKETBANK', '\u8d34\u73b0\u94f6\u884c'), (b'ACCEPTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')]),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='operator_member',
            field=models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'PAYER', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'TICKETBANK', '\u8d34\u73b0\u94f6\u884c'), (b'ACCEPTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')]),
        ),
    ]
