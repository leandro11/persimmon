# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0012_auto_20141126_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='fax_number',
            field=models.CharField(default=-232114, max_length=11, verbose_name='\u4f20\u771f\u53f7', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', '\u8bf7\u8f93\u5165\u5408\u6cd5\u7684\u4f20\u771f\u53f7', b'fax_invalid')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='mobile_number',
            field=models.CharField(default=13333334454L, max_length=14, verbose_name='\u624b\u673a\u53f7', validators=[django.core.validators.RegexValidator(b'^[\\d+]+$', '\u8bf7\u8f93\u5165\u5408\u6cd5\u7684\u624b\u673a\u53f7', b'mobile_invalid')]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='staff',
            name='telephone',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='\u56fa\u5b9a\u7535\u8bdd', validators=[django.core.validators.RegexValidator(b'^[\\d-]+$', '\u8bf7\u8f93\u5165\u5408\u6cd5\u7684\u7535\u8bdd\u53f7\u7801', b'telephone_invalid')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='staff',
            name='name',
            field=models.CharField(help_text='\u5fc5\u586b', max_length=50, verbose_name='\u59d3\u540d', validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
