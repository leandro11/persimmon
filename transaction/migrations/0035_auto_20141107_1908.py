# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0034_auto_20141107_0510'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionclaim',
            options={'verbose_name': '\u8d34\u73b0\u7533\u8bf7\u8bb0\u5f55', 'verbose_name_plural': '\u8d34\u73b0\u7533\u8bf7\u8bb0\u5f55', 'permissions': (('confirm_transactionclaim', '\u5ba1\u6838\u8d34\u73b0\u7533\u8bf7'),)},
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='available_time',
            field=models.DateTimeField(default=None, null=True, verbose_name='\u6fc0\u6d3b\u65f6\u95f4', blank=True),
        ),
    ]
