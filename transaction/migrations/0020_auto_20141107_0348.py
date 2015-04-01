# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0019_remove_transactionoperation_operate_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionmetaoperation',
            old_name='operate_type',
            new_name='operation_type',
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='operation_type',
            field=models.CharField(default=b'CONFIRM', max_length=30, verbose_name='\u64cd\u4f5c\u7c7b\u578b', choices=[(b'UPLOAD', '\u4e0a\u4f20'), (b'CONFIRM', '\u786e\u8ba4'), (b'EMS', '\u90ae\u5bc4')]),
            preserve_default=True,
        ),
    ]
