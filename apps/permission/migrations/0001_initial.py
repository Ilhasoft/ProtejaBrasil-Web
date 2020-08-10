# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Module',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nome do módulo. Ex.: Usuário, Denúncia, Rede de proteção', max_length=255, verbose_name='Nome')),
                ('alias', models.CharField(help_text='Apelido do módulo (escrito em letras minúsculas e sem acentuação. Ex.: usuario, denuncia, redes_de_protecao.)', max_length=255, verbose_name='Apelido')),
            ],
            options={
                'verbose_name_plural': 'Módulos',
                'verbose_name': 'Módulo',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='Nome da permissão. Ex.: Adicionar usuário, Editar usuário', max_length=255, verbose_name='Nome')),
                ('alias', models.CharField(help_text='Apelido da permissão (escrito em letras minúsculas e sem acentuação. Ex.: add_usuario, edit_denuncia, add_redes_de_protecao.)', max_length=255, verbose_name='Apelido')),
                ('module', models.ForeignKey(to='permission.Module', help_text='Selecione o módulo que a permissão pertence', verbose_name='Módulo')),
            ],
            options={
                'verbose_name_plural': 'Permissões',
                'verbose_name': 'Permissão',
            },
        ),
    ]
