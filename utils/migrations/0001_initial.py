# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TemplateAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u6587\u4ef6\u540d\u79f0', choices=[('\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae', '\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u534f\u8bae', '\u59d4\u6258\u4ee3\u7406\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u58f0\u660e', '\u59d4\u6258\u4ee3\u7406\u58f0\u660e'), ('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u534f\u8bae', '\u6267\u884c\u534f\u8bae'), ('\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e', '\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e'), ('\u627f\u5151\u6c47\u7968', '\u627f\u5151\u6c47\u7968')])),
                ('file', models.FileField(upload_to=b'.', verbose_name='\u6587\u4ef6')),
                ('extension', models.CharField(max_length=10, verbose_name='\u6269\u5c55\u540d', choices=[('\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae', '\u8bda\u4fe1\u5408\u4f5c\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u534f\u8bae', '\u59d4\u6258\u4ee3\u7406\u534f\u8bae'), ('\u59d4\u6258\u4ee3\u7406\u58f0\u660e', '\u59d4\u6258\u4ee3\u7406\u58f0\u660e'), ('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u534f\u8bae', '\u6267\u884c\u534f\u8bae'), ('\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e', '\u627f\u5151\u6c47\u7968\u4ea4\u63a5\u5355\u636e'), ('\u627f\u5151\u6c47\u7968', '\u627f\u5151\u6c47\u7968')])),
                ('size', models.IntegerField(max_length=10, verbose_name='\u5927\u5c0f')),
            ],
            options={
                'verbose_name': '\u9644\u4ef6\u6a21\u677f',
                'verbose_name_plural': '\u9644\u4ef6\u6a21\u677f',
            },
            bases=(models.Model,),
        ),
    ]
