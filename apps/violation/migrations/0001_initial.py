# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('protectionnetwork', '0001_initial'),
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeProtectionNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('typeprotectionnetwork', models.ForeignKey(verbose_name='Tipo de rede de proteção', to='protectionnetwork.Type')),
            ],
            options={
                'verbose_name_plural': 'Tipos de rede de proteção da violação',
                'verbose_name': 'Tipo de rede de proteção da violação',
            },
        ),
        migrations.CreateModel(
            name='TypeViolation',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nome', unique=True)),
                ('description', models.TextField(help_text='Insira uma descrição para o tipo de violação.', verbose_name='Descrição')),
                ('color', models.CharField(help_text='Informe o código hexadecimal da cor', verbose_name='Cor', max_length=10, blank=True, null=True)),
                ('icon', sorl.thumbnail.fields.ImageField(upload_to='violation/types', max_length=255, help_text='Selecione um ícone', blank=True, verbose_name='Ícone', null=True)),
                ('action', models.TextField(help_text='Insira a ação a ser tomada.', verbose_name='Ação')),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', verbose_name='Data de cadastro', auto_now_add=True)),
                ('theme', models.ForeignKey(to='theme.Theme', help_text='Selecione o tema do tipo de violação.', verbose_name='Tema')),
            ],
            options={
                'verbose_name_plural': 'Tipos',
                'verbose_name': 'Tipo',
            },
        ),
        migrations.AddField(
            model_name='typeprotectionnetwork',
            name='typeviolation',
            field=models.ForeignKey(related_name='typesprotectionnetwork', to='violation.TypeViolation', verbose_name='Tipo de violação'),
        ),
    ]
