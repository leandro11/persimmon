# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0033_auto_20141226_2217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='execution_agreements',
            field=models.ImageField(max_length=200, upload_to=b'./bank/', null=True, verbose_name='\u6267\u884c\u5408\u4f5c\u534f\u8bae', blank=True),
        ),
        migrations.AlterField(
            model_name='bank',
            name='strategic_agreements',
            field=models.ImageField(max_length=200, upload_to=b'./bank/', null=True, verbose_name='\u6218\u7565\u5408\u4f5c\u534f\u8bae', blank=True),
        ),
    ]
