# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0052_auto_20141222_1109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionoperation',
            name='upload_file',
            field=models.FileField(upload_to=b'./operation/', null=True, verbose_name='\u9644\u4ef6', blank=True),
        ),
    ]
