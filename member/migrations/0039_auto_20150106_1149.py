# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0038_auto_20141230_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bank',
            name='short_name',
            field=models.CharField(unique=True, max_length=20, verbose_name='\u94f6\u884c\u7b80\u79f0', validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='bankcontactor',
            name='bank',
            field=models.OneToOneField(related_name=b'contactor', verbose_name='\u6240\u5c5e\u94f6\u884c', to='member.Bank'),
        ),
        migrations.AlterField(
            model_name='bankoperator',
            name='bank',
            field=models.ForeignKey(related_name=b'operator_set', verbose_name='\u6240\u5c5e\u94f6\u884c', to='member.Bank'),
        ),
        migrations.AlterField(
            model_name='enterprisecontactor',
            name='enterprise',
            field=models.OneToOneField(related_name=b'contactor', verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise'),
        ),
        migrations.AlterField(
            model_name='enterpriseoperator',
            name='enterprise',
            field=models.OneToOneField(related_name=b'operator', verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise'),
        ),
    ]
