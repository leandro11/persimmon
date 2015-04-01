# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0014_auto_20141128_1137'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='staff',
            options={'verbose_name': '\u5de5\u4f5c\u4eba\u5458', 'verbose_name_plural': '\u5de5\u4f5c\u4eba\u5458'},
        ),
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.CharField(max_length=50, verbose_name='\u90ae\u4ef6\u5730\u5740', validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='staff',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='\u7528\u6237\u6709\u6548'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='name',
            field=models.CharField(unique=True, max_length=50, verbose_name='\u59d3\u540d', validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
