# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u7701\u4efd\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u7701\u4efd',
                'verbose_name_plural': '\u7701\u4efd',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='\u5fc5\u586b', max_length=50, verbose_name='\u5168\u540d', validators=[django.core.validators.MinLengthValidator(2)])),
                ('first_name', models.CharField(help_text='\u5fc5\u586b', max_length=20, verbose_name='\u59d3', validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(help_text='\u5fc5\u586b', max_length=20, verbose_name='\u540d', validators=[django.core.validators.MinLengthValidator(2)])),
                ('email', models.CharField(help_text='\u5fc5\u586b', max_length=50, verbose_name='\u90ae\u4ef6\u5730\u5740', validators=[django.core.validators.MinLengthValidator(2)])),
                ('password', models.CharField(help_text='\u5fc5\u586b', max_length=50, verbose_name='\u5bc6\u7801', validators=[django.core.validators.MinLengthValidator(2)])),
                ('is_active', models.BooleanField(default=False, verbose_name='\u7528\u6237\u72b6\u6001')),
                ('last_login', models.DateTimeField(null=True, verbose_name='\u4e0a\u6b21\u767b\u5f55\u65f6\u95f4')),
                ('date_joined', models.DateTimeField(null=True, verbose_name='\u6ce8\u518c\u65f6\u95f4')),
                ('department', models.CharField(help_text='\u5fc5\u586b', max_length=300, verbose_name='\u90e8\u95e8', validators=[django.core.validators.MinLengthValidator(2)])),
                ('position', models.CharField(help_text='\u5fc5\u586b', max_length=300, verbose_name='\u804c\u4f4d', validators=[django.core.validators.MinLengthValidator(2)])),
                ('city', models.CharField(max_length=20, verbose_name='\u57ce\u5e02')),
                ('province', models.ForeignKey(verbose_name='\u7701\u4efd', to='management.Province')),
            ],
            options={
                'verbose_name': '\u5de5\u4f5c\u4eba\u5458',
                'verbose_name_plural': '\u5de5\u4f5c\u4eba\u5458',
                'permissions': (('register', '\u5e73\u53f0\u5de5\u4f5c\u4eba\u5458\u6ce8\u518c'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20, verbose_name='\u533a\u57df\u540d\u79f0')),
            ],
            options={
                'verbose_name': '\u533a\u57df',
                'verbose_name_plural': '\u533a\u57df\u5212\u5206',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='province',
            name='zone',
            field=models.ForeignKey(verbose_name='\u6240\u5c5e\u533a\u57df', to='management.Zone'),
            preserve_default=True,
        ),
    ]
