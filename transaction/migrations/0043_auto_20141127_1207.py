# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0042_auto_20141127_1206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionclaim',
            name='payee_debt_promise',
            field=models.BooleanField(default=False, help_text=b'\xe6\x89\xbf\xe8\xaf\xba\xe8\xbf\x9e\xe5\x90\x8c\xe8\xb4\xb4\xe7\x8e\xb0\xe8\xb4\xb7\xe6\xac\xbe\xef\xbc\x8c\xe4\xbc\x81\xe4\xb8\x9a\xe7\x9a\x84\xe8\xb5\x84\xe4\xba\xa7\xe8\xb4\x9f\xe5\x80\xba\xe7\x8e\x87\xe4\xb8\x8d\xe9\xab\x98\xe4\xba\x8e70%', verbose_name='\u4f01\u4e1a\u8d1f\u503a\u627f\u8bfa'),
        ),
    ]
