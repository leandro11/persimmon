# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0008_auto_20141106_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='need_confirm',
            field=models.BooleanField(default=False, verbose_name='\u9700\u786e\u8ba4'),
        ),
    ]
