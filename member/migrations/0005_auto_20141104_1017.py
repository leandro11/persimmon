# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20141104_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterpriseoperator',
            name='enterprise',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u4f01\u4e1a', to='member.Enterprise'),
        ),
    ]
