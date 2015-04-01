# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0003_auto_20141106_1756'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionticket',
            old_name='bill_bank',
            new_name='ticket_bank',
        ),
    ]
