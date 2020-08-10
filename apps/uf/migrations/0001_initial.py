# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UF',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('initials', models.CharField(help_text='Insira a sigla do estado', max_length=3, verbose_name='Sigla', unique=True)),
                ('title', models.CharField(help_text='Insira o título do estado', max_length=100, verbose_name='Nome do estado')),
            ],
            options={
                'verbose_name_plural': 'Estados',
                'verbose_name': 'Estado',
            },
        ),
    ]
