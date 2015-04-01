# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0022_auto_20141107_0357'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transactionoperation',
            old_name='verify_service',
            new_name='confirm_service',
        ),
        migrations.AddField(
            model_name='transactionoperation',
            name='need_confirm',
            field=models.BooleanField(default=False, verbose_name='\u9700\u5ba2\u670d\u786e\u8ba4'),
            preserve_default=True,
        ),
    ]
