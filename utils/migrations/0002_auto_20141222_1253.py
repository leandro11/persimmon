# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='extension',
            field=models.CharField(max_length=10, verbose_name='\u6269\u5c55\u540d', choices=[('\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae', '\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u534f\u8bae', '\u59d4\u6258\u4ee3\u7406\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u58f0\u660e', '\u59d4\u6258\u4ee3\u7406\u58f0\u660e'), ('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u534f\u8bae', '\u6267\u884c\u534f\u8bae'), ('\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e', '\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e'), ('\u627f\u5151\u6c47\u7968', '\u627f\u5151\u6c47\u7968'), ('\u627f\u8bfa\u4e661', '\u627f\u8bfa\u4e661'), ('\u627f\u8bfa\u4e662', '\u627f\u8bfa\u4e662')]),
        ),
        migrations.AlterField(
            model_name='templateattachment',
            name='name',
            field=models.CharField(max_length=20, verbose_name='\u6587\u4ef6\u7c7b\u578b', choices=[('\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae', '\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u534f\u8bae', '\u59d4\u6258\u4ee3\u7406\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u58f0\u660e', '\u59d4\u6258\u4ee3\u7406\u58f0\u660e'), ('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u534f\u8bae', '\u6267\u884c\u534f\u8bae'), ('\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e', '\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e'), ('\u627f\u5151\u6c47\u7968', '\u627f\u5151\u6c47\u7968'), ('\u627f\u8bfa\u4e661', '\u627f\u8bfa\u4e661'), ('\u627f\u8bfa\u4e662', '\u627f\u8bfa\u4e662')]),
        ),
        migrations.AlterField(
            model_name='templateattachment',
            name='size',
            field=models.IntegerField(max_length=10, verbose_name='\u6587\u4ef6\u5927\u5c0f'),
        ),
    ]
