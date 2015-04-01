# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import member.models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0029_bankattachment_enterpriseattachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankattachment',
            name='creator',
            field=models.ForeignKey(verbose_name='\u64cd\u4f5c\u7528\u6237', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bankattachment',
            name='file',
            field=models.FileField(upload_to=member.models.get_bank_attachment_path, verbose_name='\u6587\u4ef6'),
        ),
        migrations.AlterField(
            model_name='bankattachment',
            name='thumbnail',
            field=models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=member.models.get_bank_attachment_thumbnail_path, null=True, verbose_name='\u7f29\u7565\u6587\u4ef6', blank=True),
        ),
        migrations.AlterField(
            model_name='bankattachment',
            name='type',
            field=models.CharField(max_length=50, verbose_name='\u9644\u4ef6\u5185\u5bb9', choices=[('\u6218\u7565\u5408\u4f5c\u534f\u8bae', '\u6218\u7565\u5408\u4f5c\u534f\u8bae'), ('\u6267\u884c\u5408\u4f5c\u534f\u8bae', '\u6267\u884c\u5408\u4f5c\u534f\u8bae')]),
        ),
        migrations.AlterField(
            model_name='enterpriseattachment',
            name='type',
            field=models.CharField(max_length=50, verbose_name='\u9644\u4ef6\u5185\u5bb9', choices=[('\u8425\u4e1a\u6267\u7167', '\u8425\u4e1a\u6267\u7167'), ('\u673a\u6784\u4ee3\u7801', '\u673a\u6784\u4ee3\u7801'), ('\u7a0e\u52a1\u767b\u8bb0\u8bc1', '\u7a0e\u52a1\u767b\u8bb0\u8bc1')]),
        ),
    ]
