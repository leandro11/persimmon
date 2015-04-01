# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20141104_1021'),
        ('transaction', '0002_auto_20141106_1756'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='formerholder',
            options={'verbose_name': '\u5386\u53f2\u6301\u7968\u4eba', 'verbose_name_plural': '\u5386\u53f2\u6301\u7968\u4eba'},
        ),
        migrations.AlterModelOptions(
            name='transactionclaim',
            options={'verbose_name': '\u8d34\u73b0\u7533\u8bf7\u8bb0\u5f55', 'verbose_name_plural': '\u8d34\u73b0\u7533\u8bf7\u8bb0\u5f55'},
        ),
        migrations.AlterModelOptions(
            name='transactionmetaoperation',
            options={'verbose_name': '\u8d34\u73b0\u6d41\u7a0b\u64cd\u4f5c\u6a21\u677f', 'verbose_name_plural': '\u8d34\u73b0\u6d41\u7a0b\u64cd\u4f5c\u6a21\u677f'},
        ),
        migrations.AlterModelOptions(
            name='transactionoperation',
            options={'verbose_name': '\u8d34\u73b0\u64cd\u4f5c', 'verbose_name_plural': '\u8d34\u73b0\u64cd\u4f5c'},
        ),
        migrations.AlterModelOptions(
            name='transactionorder',
            options={'verbose_name': '\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', 'verbose_name_plural': '\u8d34\u73b0\u670d\u52a1\u8ba2\u5355'},
        ),
        migrations.AlterModelOptions(
            name='transactiontype',
            options={'verbose_name': '\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', 'verbose_name_plural': '\u8d34\u73b0\u670d\u52a1\u7c7b\u578b'},
        ),
        migrations.RenameField(
            model_name='transactionclaim',
            old_name='bill_bank',
            new_name='ticket_bank',
        ),
        migrations.RenameField(
            model_name='transactionclaim',
            old_name='bill_number',
            new_name='ticket_number',
        ),
        migrations.RenameField(
            model_name='transactionorder',
            old_name='bill_number',
            new_name='ticket_number',
        ),
        migrations.RemoveField(
            model_name='transactionorder',
            name='bill_bank',
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='claim',
            field=models.ForeignKey(default=1, verbose_name='\u8d34\u73b0\u53d1\u8d77\u8bb0\u5f55', to='transaction.TransactionClaim'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='name',
            field=models.CharField(default='', unique=True, max_length=50, verbose_name='\u6301\u7968\u4eba\u540d\u79f0'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='transactionorder',
            name='ticket_bank',
            field=models.ForeignKey(related_name=b'ticket_bank', default=1, verbose_name='\u8d34\u73b0\u94f6\u884c', to='member.Bank'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='operator',
            field=models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'TICKETBANK', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'CONVERTBANK', '\u8d34\u73b0\u94f6\u884c'), (b'CONVERTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')]),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='operator_member',
            field=models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'TICKETBANK', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'CONVERTBANK', '\u8d34\u73b0\u94f6\u884c'), (b'CONVERTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')]),
        ),
    ]
