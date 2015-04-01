# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0003_auto_20141222_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='extension',
            field=models.CharField(max_length=10, null=True, verbose_name='\u6269\u5c55\u540d', blank=True),
        ),
        migrations.AlterField(
            model_name='templateattachment',
            name='size',
            field=models.DecimalField(help_text='\u5355\u4f4dKB', verbose_name='\u6587\u4ef6\u5927\u5c0f', max_digits=10, decimal_places=2),
        ),
    ]
