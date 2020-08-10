# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('identifier', models.CharField(verbose_name='Local da aplicação', max_length=255)),
                ('description', models.TextField(verbose_name='Descrição', null=True)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
            ],
            options={
                'verbose_name': 'Log',
                'verbose_name_plural': 'Logs',
            },
        ),
    ]
