# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0026_auto_20141128_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='execution_agreements',
            field=models.ImageField(upload_to=b'.', max_length=200, verbose_name='\u6267\u884c\u5408\u4f5c\u534f\u8bae'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='strategic_agreements',
            field=models.ImageField(upload_to=b'.', max_length=200, verbose_name='\u6218\u7565\u5408\u4f5c\u534f\u8bae'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='licence',
            field=models.ImageField(upload_to=b'.', max_length=200, verbose_name='\u8425\u4e1a\u6267\u7167'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='organization_code',
            field=models.ImageField(upload_to=b'.', max_length=200, verbose_name='\u7ec4\u7ec7\u4ee3\u7801\u8bc1'),
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='tax_registration',
            field=models.ImageField(upload_to=b'.', max_length=200, verbose_name='\u7a0e\u52a1\u767b\u8bb0\u8bc1'),
        ),
    ]
