# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0023_auto_20141107_0359'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionoperation',
            name='sequence',
            field=models.SmallIntegerField(default=1, max_length=5, verbose_name='\u987a\u5e8f'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='transactionoperation',
            options={'ordering': ('sequence',), 'verbose_name': '\u8d34\u73b0\u64cd\u4f5c', 'verbose_name_plural': '\u8d34\u73b0\u64cd\u4f5c'},
        ),


        migrations.AlterField(
            model_name='transactionoperation',
            name='operator_user',
            field=models.ForeignKey(verbose_name='\u6267\u884c\u4eba', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
