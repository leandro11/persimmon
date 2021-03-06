# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_auto_20141222_1253'),
    ]

    operations = [
        migrations.AddField(
            model_name='templateattachment',
            name='need_login',
            field=models.BooleanField(default=True, help_text='\u9700\u8981\u767b\u9646\u624d\u80fd\u4e0b\u8f7d', verbose_name='\u9700\u8981\u767b\u9646'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='templateattachment',
            name='type',
            field=models.CharField(default='', max_length=50, verbose_name='\u6587\u4ef6\u7c7b\u578b', choices=[('\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae', '\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u534f\u8bae', '\u59d4\u6258\u4ee3\u7406\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u58f0\u660e', '\u59d4\u6258\u4ee3\u7406\u58f0\u660e'), ('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u534f\u8bae', '\u6267\u884c\u534f\u8bae'), ('\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e', '\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e'), ('\u627f\u5151\u6c47\u7968', '\u627f\u5151\u6c47\u7968'), ('\u627f\u8bfa\u4e661', '\u627f\u8bfa\u4e661'), ('\u627f\u8bfa\u4e662', '\u627f\u8bfa\u4e662')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='templateattachment',
            name='name',
            field=models.CharField(max_length=50, verbose_name='\u6587\u4ef6\u540d\u79f0'),
        ),
    ]
