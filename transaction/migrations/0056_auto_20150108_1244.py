# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0055_auto_20150106_1149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionclaim',
            name='accept_bank',
            field=models.CharField(help_text=b'*\xe5\xbf\x85\xe5\xa1\xab', max_length=50, verbose_name='\u627f\u5151\u94f6\u884c'),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='amount',
            field=models.DecimalField(help_text=b'*\xe5\xbf\x85\xe5\xa1\xab', verbose_name='\u91d1\u989d', max_digits=11, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='pay_enterprise',
            field=models.CharField(help_text=b'*\xe5\xbf\x85\xe5\xa1\xab', max_length=50, verbose_name='\u4ed8\u6b3e\u4f01\u4e1a'),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_asset_size',
            field=models.DecimalField(help_text=b'\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe4\xb8\x87\xe5\x85\x83 *\xe5\xbf\x85\xe5\xa1\xab', verbose_name='\u8d44\u4ea7\u89c4\u6a21', max_digits=11, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_bad_credit',
            field=models.TextField(help_text=b'', max_length=500, null=True, verbose_name='\u6536\u6b3e\u65b9\u4e0d\u826f\u4fe1\u5f81', blank=True),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_debt_promise',
            field=models.BooleanField(default=False, help_text=b'\xe6\x89\xbf\xe8\xaf\xba\xe8\xbf\x9e\xe5\x90\x8c\xe8\xb4\xb4\xe7\x8e\xb0\xe8\xb4\xb7\xe6\xac\xbe\xef\xbc\x8c\xe4\xbc\x81\xe4\xb8\x9a\xe7\x9a\x84\xe8\xb5\x84\xe4\xba\xa7\xe8\xb4\x9f\xe5\x80\xba\xe7\x8e\x87\xe4\xb8\x8d\xe9\xab\x98\xe4\xba\x8e70% *\xe5\xbf\x85\xe5\xa1\xab', verbose_name='\u4f01\u4e1a\u8d1f\u503a\u7387\u627f\u8bfa'),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_net_income',
            field=models.DecimalField(help_text=b'\xe5\x8d\x95\xe4\xbd\x8d\xef\xbc\x9a\xe4\xb8\x87\xe5\x85\x83 *\xe5\xbf\x85\xe5\xa1\xab', verbose_name='\u8425\u6536\u5165\u989d', max_digits=11, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_rate_file',
            field=models.ImageField(help_text=b'<a target="_blank" href="">\xe9\x93\xb6\xe8\xa1\x8c\xe8\xaf\x84\xe7\xba\xa7\xe8\xaf\xb4\xe6\x98\x8e</a>', upload_to=b'.', null=True, verbose_name='\u94f6\u884c\u8bc4\u7ea7\u626b\u63cf\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='status',
            field=models.CharField(default=b'PENDING', max_length=20, verbose_name='\u8d34\u73b0\u53d1\u8d77\u72b6\u6001', choices=[(b'PENDING', '\u5f85\u5ba1\u6838'), (b'PASSED', '\u5df2\u901a\u8fc7'), (b'ABORT', '\u5df2\u4f5c\u5e9f')]),
        ),
        migrations.AlterField(
            model_name='transactionclaim',
            name='ticket_bank',
            field=models.CharField(help_text=b'*\xe5\xbf\x85\xe5\xa1\xab', max_length=50, verbose_name='\u8d34\u73b0\u94f6\u884c'),
        ),
    ]
