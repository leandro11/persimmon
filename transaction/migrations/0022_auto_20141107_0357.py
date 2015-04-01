# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0021_auto_20141107_0355'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionoperation',
            old_name='attachment',
            new_name='upload_file',
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='need_ems',
            field=models.BooleanField(default=False, verbose_name='\u9700\u8981EMS'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='need_upload',
            field=models.BooleanField(default=False, verbose_name='\u9700\u8981\u4e0a\u4f20'),
            preserve_default=True,
        ),
    ]
