# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20141104_1021'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormerHolder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50, verbose_name='\u6301\u7968\u4eba\u540d\u79f0')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionClaim',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill_number', models.CharField(unique=True, max_length=50, verbose_name='\u6c47\u7968\u5355\u53f7')),
                ('receivable_enterprise', models.CharField(max_length=50, verbose_name='\u6536\u6b3e\u4f01\u4e1a')),
                ('pay_enterprise', models.CharField(max_length=50, verbose_name='\u4ed8\u6b3e\u4f01\u4e1a')),
                ('bill_bank', models.CharField(max_length=50, verbose_name='\u8d34\u73b0\u94f6\u884c')),
                ('accept_bank', models.CharField(max_length=50, verbose_name='\u627f\u5151\u94f6\u884c')),
                ('amount', models.DecimalField(verbose_name='\u91d1\u989d', max_digits=11, decimal_places=2)),
                ('status', models.CharField(default=b'PENGDING', max_length=20, verbose_name='\u8d34\u73b0\u53d1\u8d77\u72b6\u6001', choices=[(b'PENGDING', '\u5f85\u5ba1\u6838'), (b'PASSED', '\u5df2\u901a\u8fc7'), (b'ABORT', '\u5df2\u4f5c\u5e9f')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionMetaOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sequence', models.SmallIntegerField(unique=True, max_length=5, verbose_name='\u987a\u5e8f')),
                ('operate_type', models.CharField(default=b'CONFIRM', max_length=30, verbose_name='\u64cd\u4f5c\u7c7b\u578b', choices=[(b'UPLOAD', '\u4e0a\u4f20'), (b'CONFIRM', '\u786e\u8ba4'), (b'EMS', '\u90ae\u5bc4')])),
                ('operator', models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'BILLBANK', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'CONVERTBANK', '\u8d34\u73b0\u94f6\u884c'), (b'CONVERTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')])),
                ('description', models.CharField(max_length=200, verbose_name='\u64cd\u4f5c\u63cf\u8ff0')),
                ('file_type', models.CharField(default=b'NONE', max_length=30, verbose_name='\u6587\u4ef6\u540d\u79f0', choices=[(b'NONE', '\u65e0\u9644\u4ef6'), (b'EXECUTION_AGREEMENT', '\u6267\u884c\u534f\u8bae'), (b'ENTRUST_DECLARATION', '\u59d4\u6258\u58f0\u660e')])),
                ('need_upload', models.BooleanField(default=False, verbose_name='\u9700\u8981\u4e0a\u4f20')),
                ('need_ems', models.BooleanField(default=False, verbose_name='\u6709EMS')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionOperation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('operator_member', models.CharField(max_length=30, verbose_name='\u6267\u884c\u65b9', choices=[(b'RECEIVER', '\u6536\u6b3e\u4f01\u4e1a'), (b'BILLBANK', '\u4ed8\u6b3e\u4f01\u4e1a'), (b'CONVERTBANK', '\u8d34\u73b0\u94f6\u884c'), (b'CONVERTBANK', '\u627f\u5151\u94f6\u884c'), (b'PLATFORM', '\u6021\u667a\u878d\u901a')])),
                ('description', models.CharField(max_length=200, verbose_name='\u64cd\u4f5c\u63cf\u8ff0')),
                ('file_type', models.CharField(default=b'NONE', max_length=30, verbose_name='\u6587\u4ef6\u540d\u79f0', choices=[(b'NONE', '\u65e0\u9644\u4ef6'), (b'EXECUTION_AGREEMENT', '\u6267\u884c\u534f\u8bae'), (b'ENTRUST_DECLARATION', '\u59d4\u6258\u58f0\u660e')])),
                ('need_upload', models.BooleanField(default=False, verbose_name='\u9700\u8981\u4e0a\u4f20')),
                ('need_ems', models.BooleanField(default=False, verbose_name='\u9700\u8981EMS')),
                ('attachment', models.FileField(upload_to=b'/', null=True, verbose_name='\u9644\u4ef6', blank=True)),
                ('ems_number', models.CharField(max_length=30, null=True, verbose_name='EMS\u5355\u53f7', blank=True)),
                ('status', models.CharField(default=b'UNACTIVATED', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'UNACTIVATED', '\u672a\u6fc0\u6d3b'), (b'ACTIVATED', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5b8c\u6210')])),
                ('remark', models.CharField(max_length=200, verbose_name='\u5907\u6ce8')),
                ('available_time', models.DateTimeField(default=None, null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
                ('finish_time', models.DateTimeField(default=None, null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
                ('operator', models.ForeignKey(verbose_name='\u6267\u884c\u4eba', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionOrder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill_number', models.CharField(unique=True, max_length=50, verbose_name='\u6c47\u7968\u5355\u53f7')),
                ('amount', models.DecimalField(verbose_name='\u91d1\u989d', max_digits=11, decimal_places=2)),
                ('status', models.CharField(default=b'START', max_length=20, verbose_name='\u8d34\u73b0\u8ba2\u5355\u72b6\u6001', choices=[(b'START', '\u65b0\u751f\u6210'), (b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'DONE', '\u5df2\u5f2f\u6c89'), (b'ABORT', '\u5df2\u4f5c\u5e9f')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('finish_time', models.DateTimeField(default=None, null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
                ('modify_time', models.DateTimeField(auto_now=True, verbose_name='\u6700\u540e\u4fee\u6539\u65f6\u95f4', auto_now_add=True)),
                ('accept_bank', models.ForeignKey(related_name=b'accept_bank', verbose_name='\u627f\u5151\u94f6\u884c', to='member.Bank')),
                ('bill_bank', models.ForeignKey(related_name=b'bill_bank', verbose_name='\u8d34\u73b0\u94f6\u884c', to='member.Bank')),
                ('pay_enterprise', models.ForeignKey(related_name=b'pay_enterprise', verbose_name='\u4ed8\u6b3e\u4f01\u4e1a', to='member.Enterprise')),
                ('receivable_enterprise', models.ForeignKey(related_name=b'receivable_enterprise', verbose_name='\u6536\u6b3e\u4f01\u4e1a', to='member.Enterprise')),
                ('transaction_claim', models.ForeignKey(verbose_name='\u6536\u6b3e\u4f01\u4e1a', to='transaction.TransactionClaim')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'CASHIN_7DAY', max_length=20, verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', choices=[(b'CASHIN_2DAY', '\u4e24\u65e5\u8d34\u73b0'), (b'CASHIN_3DAY', '\u4e09\u65e5\u8d34\u73b0'), (b'CASHIN_5DAY', '\u4e94\u65e5\u8d34\u73b0'), (b'CASHIN_7DAY', '\u4e03\u65e5\u8d34\u73b0')])),
                ('fee', models.DecimalField(verbose_name='\u670d\u52a1\u8d39\u7387', max_digits=10, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='transactionorder',
            name='type',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', to='transaction.TransactionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='order',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='verify_service',
            field=models.ForeignKey(verbose_name='\u5ba1\u6838\u5ba2\u670d', blank=True, to='management.Staff', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionmetaoperation',
            name='trsaction_type',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', to='transaction.TransactionType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formerholder',
            name='claim',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u53d1\u8d77\u8bb0\u5f55', to='transaction.TransactionClaim'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formerholder',
            name='order',
            field=models.ForeignKey(verbose_name='\u8d34\u73b0\u670d\u52a1\u8ba2\u5355', to='transaction.TransactionOrder'),
            preserve_default=True,
        ),
    ]
