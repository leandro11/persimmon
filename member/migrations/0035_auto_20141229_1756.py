# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0034_auto_20141229_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterprise',
            name='licence',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='\u8425\u4e1a\u6267\u7167', blank=True),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='organization_code',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='\u7ec4\u7ec7\u4ee3\u7801\u8bc1', blank=True),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='tax_registration',
            field=models.ImageField(upload_to=b'.', null=True, verbose_name='\u7a0e\u52a1\u767b\u8bb0\u8bc1', blank=True),
        ),
    ]
