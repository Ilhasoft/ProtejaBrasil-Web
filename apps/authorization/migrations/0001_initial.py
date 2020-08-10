# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('application', models.CharField(help_text='Insira o nome da aplicação que usará o token gerado.', max_length=255, verbose_name='Aplicação')),
                ('token', models.CharField(help_text='Token de autorização', max_length=30, verbose_name='Token', unique=True)),
                ('is_active', models.BooleanField(help_text='Selecione se deseja permitir que esse aplicativo consulte a API', verbose_name='Ativo', default=True)),
            ],
            options={
                'verbose_name_plural': 'Tokens',
                'verbose_name': 'Token',
            },
        ),
    ]
