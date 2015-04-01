# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0041_auto_20141127_1131'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionclaim',
            old_name='receivable_enterprise_rate_file',
            new_name='payee_rate_file',
        ),
        migrations.RemoveField(
            model_name='transactionclaim',
            name='receivable_enterprise_rate',
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='payee_asset_size',
            field=models.DecimalField(default=None, help_text=b'\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe4\xb8\x87\xe5\x85\x83', verbose_name='\u8d44\u4ea7\u89c4\u6a21', max_digits=11, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='payee_bad_credit',
            field=models.TextField(help_text=b'\xe6\x97\xa0\xe4\xb8\x8d\xe8\x89\xaf\xe4\xbf\xa1\xe5\xbe\x81\xe8\xae\xb0\xe5\xbd\x95\xe5\x8f\xaf\xe4\xb8\x8d\xe5\xa1\xab', max_length=500, null=True, verbose_name='\u6536\u6b3e\u65b9\u4e0d\u826f\u4fe1\u5f81', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='payee_debt_promise',
            field=models.BooleanField(default=False, help_text=b'\xe6\x89\xbf\xe8\xaf\xba\xe8\xbf\x9e\xe5\x90\x8c\xe8\xb4\xb4\xe7\x8e\xb0\xe8\xb4\xb7\xe6\xac\xbe\xef\xbc\x8c\xe4\xbc\x81\xe4\xb8\x9a\xe7\x9a\x84\xe8\xb5\x84\xe4\xba\xa7\xe8\xb4\x9f\xe5\x80\xba\xe7\x8e\x87\xe4\xb8\x8d\xe9\xab\x98\xe4\xba\x8e70%', verbose_name='\u4f01\u4e1a\u8d1f\u503a\u627f\u8bfa'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='payee_net_income',
            field=models.DecimalField(default=0, help_text=b'\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe4\xb8\x87\xe5\x85\x83', verbose_name='\u8425\u6536\u5165\u989d', max_digits=11, decimal_places=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='payee_rate',
            field=models.CharField(max_length=50, null=True, verbose_name='\u6536\u6b3e\u65b9\u94f6\u884c\u8bc4\u7ea7', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionclaim',
            name='ticket_deadline',
            field=models.DateField(null=True, verbose_name='\u6c47\u7968\u671f\u9650'),
            preserve_default=True,
        ),
    ]
