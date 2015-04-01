# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0012_auto_20141229_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='SMSVerifyCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=50, verbose_name='\u9a8c\u8bc1\u7801\u7c7b\u578b', choices=[(b'MEMBER_REGISTRATION', b'\xe4\xbc\x9a\xe5\x91\x98\xe6\xb3\xa8\xe5\x86\x8c'), (b'BANK_CONTACTOR_MOBILE', b'\xe9\x93\xb6\xe8\xa1\x8c\xe4\xb8\xbb\xe8\x81\x94\xe7\xbb\x9c\xe4\xba\xba\xe6\x89\x8b\xe6\x9c\xba\xe9\xaa\x8c\xe8\xaf\x81'), (b'BANK_OPERATOR_MOBILE', b'\xe9\x93\xb6\xe8\xa1\x8c\xe6\x89\xa7\xe8\xa1\x8c\xe4\xba\xba\xe6\x89\x8b\xe6\x9c\xba\xe9\xaa\x8c\xe8\xaf\x81'), (b'ENTERPRISE_CONTACTOR_MOBILE', b'\xe4\xbc\x81\xe4\xb8\x9a\xe4\xb8\xbb\xe8\x81\x94\xe7\xbb\x9c\xe4\xba\xba\xe6\x89\x8b\xe6\x9c\xba\xe9\xaa\x8c\xe8\xaf\x81'), (b'ENTERPRISE_OPERATOR_MOBILE', b'\xe4\xbc\x81\xe4\xb8\x9a\xe6\x89\xa7\xe8\xa1\x8c\xe4\xba\xba\xe6\x89\x8b\xe6\x9c\xba\xe9\xaa\x8c\xe8\xaf\x81')])),
                ('key', models.CharField(unique=True, max_length=50, verbose_name='\u9a8c\u8bc1\u7801\u6807\u8bc6')),
                ('mobile', models.CharField(max_length=13, verbose_name='\u624b\u673a\u53f7\u7801', validators=[django.core.validators.RegexValidator(b'^[\\d+]+$', '\u624b\u673a\u53f7\u7801\u4e0d\u6b63\u786e', b'mobile_invalid')])),
                ('code', models.PositiveSmallIntegerField(blank=True, max_length=8, null=True, verbose_name='\u9a8c\u8bc1\u7801', validators=[django.core.validators.RegexValidator(b'^[\\d+]+$', '\u9a8c\u8bc1\u7801\u683c\u5f0f\u4e0d\u6b63\u786e', b'code_invalid')])),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
