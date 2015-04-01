# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0016_auto_20141124_1703'),
    ]

    operations = [
        migrations.RenameField(
            model_name='registerinvitationcode',
            old_name='operator',
            new_name='market_manager',
        ),
        migrations.AlterField(
            model_name='enterprise',
            name='invite_code',
            field=models.OneToOneField(null=True, blank=True, to='member.RegisterInvitationCode', verbose_name='\u9080\u8bf7\u7801'),
        ),
        migrations.AlterField(
            model_name='registerinvitationcode',
            name='status',
            field=models.CharField(default=b'Activated', max_length=10, verbose_name='\u9080\u8bf7\u7801\u72b6\u6001', choices=[(b'PENDING', '\u5f85\u5ba1\u6838'), (b'Activated', '\u672a\u4f7f\u7528'), (b'Used', '\u5df2\u4f7f\u7528'), (b'Inactived', '\u5df2\u4f5c\u5e9f')]),
        ),
    ]
