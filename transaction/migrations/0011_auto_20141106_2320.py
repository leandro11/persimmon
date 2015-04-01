# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0010_auto_20141106_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionmetaoperation',
            name='sequence',
            field=models.SmallIntegerField(max_length=5, verbose_name='\u987a\u5e8f'),
        ),
        migrations.AlterUniqueTogether(
            name='transactionmetaoperation',
            unique_together=set([('trsaction_type', 'sequence')]),
        ),
    ]
