# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from apps.theme.models import ThemeInternationalization


def populate_theme_internationalization(apps, schema_editor):
    model = apps.get_model('theme', 'Theme')
    for row in model.objects.all():
        if row.info.all().count() == 0:
            ThemeInternationalization.objects.create(row.id, 'pt', row.title, row.description)


class Migration(migrations.Migration):
    dependencies = [
        ('theme', '0005_theme_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='ThemeInternationalization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('language', models.CharField(choices=[('pt', 'Português'), ('en', 'English'), ('es', 'Español')], default='pt', max_length=2, verbose_name='Idioma')),
                ('title', models.CharField(verbose_name='Título', help_text='Insira o título do tema', max_length=255)),
                ('description', models.TextField(verbose_name='Descrição', blank=True, null=True)),
                ('date_joined', models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro', auto_now_add=True)),
                ('theme', models.ForeignKey(related_name='info', verbose_name='Tema', help_text='Tema', to='theme.Theme')),
            ],
        ),
        migrations.RunPython(
            code=populate_theme_internationalization,
            atomic=True
        ),
    ]
