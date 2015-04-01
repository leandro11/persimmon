# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0044_auto_20141127_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transactionclaim',
            name='ticket_deadline',
            field=models.DateField(null=True, verbose_name='\u6c47\u7968\u671f\u9650'),
        ),
    ]
