# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0016_auto_20141107_0309'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionoperation',
            name='operator_member_id',
            field=models.BigIntegerField(default=1, max_length=30, verbose_name='\u6267\u884c\u65b9\u7f16\u53f7'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='operator_type',
            field=models.CharField(default='\u6021\u667a\u878d\u901a', max_length=30, verbose_name='\u6267\u884c\u65b9\u7c7b\u578b', choices=[('\u94f6\u884c\u4f1a\u5458', '\u94f6\u884c\u4f1a\u5458'), ('\u94f6\u884c\u4f1a\u5458', '\u94f6\u884c\u4f1a\u5458'), ('\u6021\u667a\u878d\u901a', '\u6021\u667a\u878d\u901a')]),
            preserve_default=True,
        ),
    ]
