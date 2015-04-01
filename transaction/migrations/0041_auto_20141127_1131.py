# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0040_transactionclaim_create_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionclaim',
            name='receivable_enterprise_rate',
            field=models.CharField(max_length=50, null=True, verbose_name='\u6536\u6b3e\u4f01\u4e1a\u94f6\u884c\u8bc4\u7ea7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='receivable_enterprise_rate_file',
            field=models.ImageField(upload_to=b'/', null=True, verbose_name='\u94f6\u884c\u8bc4\u7ea7\u626b\u63cf\u4ef6', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='ticket_number',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u6c47\u7968\u5355\u53f7', blank=True),
        ),
    ]
