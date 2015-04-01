# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0054_auto_20141230_2342'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transactionclaim',
            options={'verbose_name': '\u8d34\u73b0\u7533\u8bf7', 'verbose_name_plural': '\u8d34\u73b0\u7533\u8bf7\u8bb0\u5f55', 'permissions': (('confirm_transactionclaim', '\u5ba1\u6838\u8d34\u73b0\u7533\u8bf7'),)},
        ),
        migrations.RemoveField(
            model_name='transactionmetaoperation',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='transactionoperation',
            name='file_type',
        ),
        migrations.RemoveField(
            model_name='transactionoperation',
            name='operator_member_id',
        ),
        migrations.RemoveField(
            model_name='transactionoperation',
            name='operator_member_type',
        ),
        migrations.AddField(
            model_name='transactionmetaoperation',
            name='file_name',
            field=models.CharField(max_length=30, null=True, verbose_name='\u9644\u4ef6\u540d\u79f0', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='file_name',
            field=models.CharField(max_length=30, null=True, verbose_name='\u9644\u4ef6\u540d\u79f0', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='description',
            field=models.TextField(max_length=500, verbose_name='\u64cd\u4f5c\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='need_confirm',
            field=models.BooleanField(default=False, verbose_name='\u9700\u5ba2\u670d\u786e\u8ba4'),
        ),
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='need_upload',
            field=models.BooleanField(default=False, verbose_name='\u9644\u4ef6\u4e0a\u4f20'),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='description',
            field=models.TextField(max_length=500, verbose_name='\u64cd\u4f5c\u63cf\u8ff0'),
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='need_upload',
            field=models.BooleanField(default=False, verbose_name='\u9644\u4ef6\u4e0a\u4f20'),
        ),
        migrations.AlterField(
            model_name='transactiontype',
            name='name',
            field=models.CharField(default='\u5c06\u5f00\u6c47\u7968\u4ee3\u7406\u89c1\u7968\u5373\u8d34\u670d\u52a1', unique=True, max_length=50, verbose_name='\u8d34\u73b0\u670d\u52a1\u7c7b\u578b', choices=[('\u5c06\u5f00\u6c47\u7968\u4ee3\u7406\u89c1\u7968\u5373\u8d34\u670d\u52a1', '\u5c06\u5f00\u6c47\u7968\u4ee3\u7406\u89c1\u7968\u5373\u8d34\u670d\u52a1'), ('\u6301\u7968\u4f01\u4e1a\u59d4\u6258\u4ee3\u7406\u89c1\u7968\u5373\u8d34\u670d\u52a1', '\u6301\u7968\u4f01\u4e1a\u59d4\u6258\u4ee3\u7406\u89c1\u7968\u5373\u8d34\u670d\u52a1'), ('\u89c1\u7968\u5373\u8d34\u671f\u6743\u670d\u52a1', '\u89c1\u7968\u5373\u8d34\u671f\u6743\u670d\u52a1')]),
        ),
    ]
