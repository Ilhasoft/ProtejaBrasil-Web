# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import geoposition.fields
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('uf', '0001_initial'),
        ('theme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingDaysProtectionNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('day', models.CharField(choices=[('sunday', 'Domingo'), ('monday', 'Segunda-feira'), ('tuesday', 'Terça-feira'), ('wednesday', 'Quarta-feira'), ('thursday', 'Quinta-feira'), ('friday', 'Sexta-feira'), ('saturday', 'Sábado')], max_length=10, verbose_name='Dia da semana')),
            ],
            options={
                'verbose_name_plural': 'Dias de atendimento',
                'verbose_name': 'Dia de atendimento',
            },
        ),
        migrations.CreateModel(
            name='ProtectionNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('position', geoposition.fields.GeopositionField(help_text='Selecione a localização no mapa.', max_length=42, verbose_name='Coordenadas')),
                ('zipcode', models.CharField(max_length=10, verbose_name='CEP')),
                ('address', models.CharField(max_length=255, verbose_name='Logradouro')),
                ('neighborhood', models.CharField(max_length=255, verbose_name='Bairro')),
                ('city', models.CharField(max_length=255, verbose_name='Cidade')),
                ('contact', models.CharField(verbose_name='Contato', max_length=255, blank=True, null=True)),
                ('phone1', models.CharField(max_length=20, verbose_name='Telefone 1')),
                ('phone2', models.CharField(verbose_name='Telefone 2', max_length=20, blank=True, null=True)),
                ('email', models.CharField(max_length=255, verbose_name='E-mail')),
                ('schedule', models.TextField(verbose_name='Horário', blank=True, null=True)),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', verbose_name='Data de cadastro', auto_now_add=True)),
                ('state', models.ForeignKey(max_length=255, to='uf.UF', verbose_name='Estado')),
            ],
            options={
                'verbose_name_plural': 'Redes de proteção',
                'verbose_name': 'Rede de proteção',
            },
        ),
        migrations.CreateModel(
            name='ThemeProtectionNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('protectionnetwork', models.ForeignKey(related_name='themes', to='protectionnetwork.ProtectionNetwork', verbose_name='Rede de proteção')),
                ('theme', models.ForeignKey(verbose_name='Tema', to='theme.Theme')),
            ],
            options={
                'verbose_name_plural': 'Temas',
                'verbose_name': 'Tema',
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Informe o nome do tipo da rede de proteção', max_length=255, verbose_name='Nome', unique=True)),
                ('color', models.CharField(help_text='Informe o código hexadecimal da cor', verbose_name='Cor', max_length=10, blank=True, null=True)),
                ('icon', sorl.thumbnail.fields.ImageField(upload_to='protectionnetwork/types', max_length=255, help_text='Selecione um ícone', blank=True, verbose_name='Ícone', null=True)),
                ('date_joined', models.DateTimeField(help_text='Data de cadastro', verbose_name='Data de cadastro', auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Tipos',
                'verbose_name': 'Tipo',
            },
        ),
        migrations.AddField(
            model_name='protectionnetwork',
            name='type',
            field=models.ForeignKey(to='protectionnetwork.Type', help_text='Selecione o tipo da rede de proteção', verbose_name='Tipo'),
        ),
        migrations.AddField(
            model_name='operatingdaysprotectionnetwork',
            name='protectionnetwork',
            field=models.ForeignKey(related_name='operatingdays', to='protectionnetwork.ProtectionNetwork', verbose_name='Rede de proteção'),
        ),
    ]
