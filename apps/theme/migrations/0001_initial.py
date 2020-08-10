# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(help_text='Insira o título do tema', max_length=255, verbose_name='Título')),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', verbose_name='Data de cadastro', auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Temas',
                'verbose_name': 'Tema',
            },
        ),
    ]
