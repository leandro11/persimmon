# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_auto_20141107_0154'),
        ('transaction', '0036_remove_transactionclaim_receivable_enterprise'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionclaim',
            name='receivable_enterprise',
            field=models.ForeignKey(default=1, verbose_name='\u6536\u6b3e\u4f01\u4e1a', to='member.Enterprise'),
            preserve_default=False,
        ),
    ]
