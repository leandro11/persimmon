# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0022_auto_20141127_1131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='fax_number',
            field=models.IntegerField(max_length=20, verbose_name='\u4f20\u771f\u53f7', validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
