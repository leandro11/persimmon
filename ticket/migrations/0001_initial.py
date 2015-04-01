# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_auto_20141104_1021'),
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(unique=True, max_length=50, verbose_name='\u53d1\u7968\u5355\u53f7')),
                ('amount', models.DecimalField(verbose_name='\u91d1\u989d', max_digits=11, decimal_places=2)),
                ('status', models.CharField(default=b'PROCESSING', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'LODGED', '\u5df2\u63d0\u4ea4'), (b'PROCESSING', '\u8fdb\u884c\u4e2d'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5b8c\u6210'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('finish_time', models.DateTimeField(default=None, null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TransactionTicket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(unique=True, max_length=50, verbose_name='\u6c47\u7968\u53f7')),
                ('amount', models.DecimalField(verbose_name='\u91d1\u989d', max_digits=11, decimal_places=2)),
                ('ems', models.CharField(unique=True, max_length=50, verbose_name='\u51fa\u7968\u5feb\u9012')),
                ('status', models.CharField(default=b'RECEIVED', max_length=30, verbose_name='\u64cd\u4f5c\u72b6\u6001', choices=[(b'RECEIVED', '\u5df2\u6536\u7968'), (b'SENT', '\u5df2\u5bc4\u51fa'), (b'ARRIVED', '\u5df2\u5bc4\u8fbe'), (b'PENDING', '\u5f85\u5ba1\u6838'), (b'FINISHED', '\u5df2\u5b8c\u6210'), (b'FINISHED', '\u5df2\u4f5c\u5e9f')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6536\u7968\u65f6\u95f4')),
                ('finish_time', models.DateTimeField(default=None, null=True, verbose_name='\u5b8c\u6210\u65f6\u95f4', blank=True)),
                ('bill_bank', models.ForeignKey(verbose_name='\u8d34\u73b0\u94f6\u884c', to='member.Bank')),
                ('conductor', models.ForeignKey(related_name=b'conductor', verbose_name='\u6838\u7968\u5458', blank=True, to='management.Staff', null=True)),
                ('director', models.ForeignKey(related_name=b'director', verbose_name='\u7968\u636e\u4e3b\u7ba1', blank=True, to='management.Staff', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
