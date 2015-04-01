# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ticket', '0002_auto_20141106_1753'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invoice',
            options={'verbose_name': '\u53d1\u7968', 'verbose_name_plural': '\u53d1\u7968'},
        ),
        migrations.AlterModelOptions(
            name='transactionticket',
            options={'verbose_name': '\u6c47\u7968', 'verbose_name_plural': '\u6c47\u7968'},
        ),
        migrations.RenameField(
            model_name='invoice',
            old_name='order',
            new_name='transaction',
        ),
        migrations.RenameField(
            model_name='transactionticket',
            old_name='order',
            new_name='transaction',
        ),
    ]
