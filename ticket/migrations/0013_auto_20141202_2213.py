# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0017_remove_staff_department'),
        ('ticket', '0012_auto_20141202_1744'),
    ]

    operations = [
        migrations.CreateModel(
            name='TicketLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('before_status', models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u524d\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838')])),
                ('after_status', models.CharField(max_length=30, verbose_name='\u53d8\u66f4\u540e\u72b6\u6001', choices=[(b'RECEIVED_PENDING', '\u6536\u7968\u5f85\u6838'), (b'RECEIVED', '\u6536\u7968\u5df2\u6838'), (b'VERIFIED_PENDING', '\u9a8c\u7968\u5f85\u6838'), (b'VERIFIED', '\u9a8c\u7968\u5df2\u6838'), (b'ARRIVE_PENDING', '\u5165\u5e93\u5f85\u6838'), (b'ARRIVED', '\u5165\u5e93\u5df2\u6838'), (b'FINISHED_PENDING', '\u51fa\u5e93\u5f85\u6838'), (b'FINISHED', '\u51fa\u5e93\u5df2\u6838')])),
                ('remarks', models.CharField(max_length=300, null=True, verbose_name='\u64cd\u4f5c\u72b6\u6001', blank=True)),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4')),
                ('operator', models.ForeignKey(verbose_name='\u6267\u884c\u4eba', to='management.Staff')),
                ('ticket', models.ForeignKey(verbose_name='\u53d1\u7968', to='ticket.TransactionTicket')),
            ],
            options={
                'verbose_name': '\u6c47\u7968\u53d8\u66f4',
                'verbose_name_plural': '\u6c47\u7968\u53d8\u66f4\u8bb0\u5f55',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='ticketelog',
            name='operator',
        ),
        migrations.RemoveField(
            model_name='ticketelog',
            name='ticket',
        ),
        migrations.DeleteModel(
            name='TicketeLog',
        ),
        migrations.AlterModelOptions(
            name='invoicelog',
            options={'verbose_name': '\u53d1\u7968\u53d8\u66f4', 'verbose_name_plural': '\u53d1\u7968\u53d8\u66f4\u8bb0\u5f55'},
        ),
        migrations.AlterField(
            model_name='invoicelog',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u64cd\u4f5c\u65f6\u95f4'),
        ),
    ]
