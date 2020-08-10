# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('type', models.CharField(max_length=20, choices=[('doubt', 'Dúvida'), ('suggestion', 'Sugestão'), ('criticism', 'Crítica'), ('compliment', 'Elogio')], verbose_name='Tipo')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('email', models.EmailField(max_length=255, verbose_name='E-mail')),
                ('message', models.TextField(verbose_name='Mensagem')),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='Data de cadastro')),
            ],
            options={
                'verbose_name_plural': 'Feedback',
                'verbose_name': 'Feedback',
            },
        ),
    ]
