# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0011_auto_20141112_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='execution_agreements',
            field=models.ImageField(upload_to=b'/', max_length=200, verbose_name='\u6267\u884c\u5408\u4f5c\u534f\u8bae'),
        ),
        migrations.AlterField(
            model_name='bank',
            name='strategic_agreements',
            field=models.ImageField(upload_to=b'/', max_length=200, verbose_name='\u6218\u7565\u5408\u4f5c\u534f\u8bae'),
        ),
    ]
