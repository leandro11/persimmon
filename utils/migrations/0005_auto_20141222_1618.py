# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0004_auto_20141222_1603'),
    ]

    operations = [
        migrations.AlterField(
            model_name='templateattachment',
            name='extension',
            field=models.CharField(max_length=10, verbose_name='\u6269\u5c55\u540d'),
        ),
        migrations.AlterField(
            model_name='templateattachment',
            name='file',
            field=models.FileField(upload_to=b'./template_document/', verbose_name='\u6587\u4ef6'),
        ),
    ]
