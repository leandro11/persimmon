# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import transaction.models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0053_auto_20141229_2311'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionoperation',
            name='upload_file_name',
            field=models.CharField(max_length=50, null=True, verbose_name='\u9644\u4ef6\u540d\u79f0', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='upload_file_thumbnail',
            field=models.FileField(help_text='\u4ec5\u56fe\u7247\u7c7b\u578b\u6587\u4ef6\u81ea\u52a8\u751f\u6210', upload_to=transaction.models.get_operation_attachment_thumbnail_path, null=True, verbose_name='\u9644\u4ef6\u7f29\u7565\u56fe', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transactionoperation',
            name='upload_file',
            field=models.FileField(upload_to=transaction.models.get_operation_attachment_path, null=True, verbose_name='\u9644\u4ef6\u6587\u4ef6', blank=True),
        ),
    ]
