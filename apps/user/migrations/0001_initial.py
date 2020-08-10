# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('uf', '0001_initial'),
        ('theme', '0001_initial'),
        ('auth', '0006_require_contenttypes_0002'),
        ('permission', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', blank=True, null=True)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(help_text='Username do usuário relacionado', max_length=30, verbose_name='Username', unique=True)),
                ('email', models.CharField(help_text='E-mail do usuário relacionado', max_length=255, verbose_name='E-mail')),
                ('first_name', models.CharField(help_text='Nome do usuário relacionado', max_length=255, verbose_name='Nome')),
                ('last_name', models.CharField(help_text='Sobrenome do usuário relacionado', max_length=255, verbose_name='Sobrenome')),
                ('phone', models.CharField(verbose_name='Telefone', max_length=100, blank=True, null=True)),
                ('cell', models.CharField(verbose_name='Celular', max_length=100, blank=True, null=True)),
                ('institution', models.CharField(verbose_name='Instituição', max_length=255, blank=True, null=True)),
                ('departament', models.CharField(verbose_name='departamento', max_length=255, blank=True, null=True)),
                ('type', models.CharField(help_text='Selecione o tipo de usuário', choices=[('theme_admin', 'Administrador do tema'), ('theme_user', 'Usuário do tema'), ('partner', 'Parceiro')], max_length=20, verbose_name='Tipo')),
                ('is_active', models.BooleanField(help_text='Determina se este usuário deve ser tratado como ativo. Desmarque esta opção em vez de excluir contas.', verbose_name='Ativo', default=True)),
                ('is_staff', models.BooleanField(help_text='Determina se o usuário pode acessar o Administrador.', verbose_name='Membro da equipe', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='Data de cadastro', default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(related_name='user_set', to='auth.Group', help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', blank=True, verbose_name='groups', related_query_name='user')),
                ('user_auth', models.ForeignKey(related_name='user_insert', to=settings.AUTH_USER_MODEL, help_text='Usuário que o cadastrou', blank=True, verbose_name='Usuário de cadastro', null=True)),
                ('user_permissions', models.ManyToManyField(related_name='user_set', to='auth.Permission', help_text='Specific permissions for this user.', blank=True, verbose_name='user permissions', related_query_name='user')),
            ],
            options={
                'verbose_name_plural': 'Usuários',
                'verbose_name': 'Usuário',
            },
        ),
        migrations.CreateModel(
            name='UsersPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('permission', models.ForeignKey(verbose_name='Permissão', to='permission.Permission')),
                ('user', models.ForeignKey(related_name='permissions', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'Permissões do usuário',
                'verbose_name': 'Permissão do usuário',
            },
        ),
        migrations.CreateModel(
            name='UsersTheme',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('theme', models.ForeignKey(verbose_name='Tema', to='theme.Theme')),
                ('user', models.ForeignKey(related_name='themes', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'Temas do usuário',
                'verbose_name': 'Tema do usuário',
            },
        ),
        migrations.CreateModel(
            name='UsersUF',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('uf', models.ForeignKey(to='uf.UF', help_text='Selecione um estado que o usuário pertence', verbose_name='UF')),
                ('user', models.ForeignKey(related_name='states', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name_plural': 'UFs do usuário',
                'verbose_name': 'UF do usuário',
            },
        ),
    ]
