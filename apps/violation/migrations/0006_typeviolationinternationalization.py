# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from apps.violation.models import TypeViolationInternationalization


def populate_typeviolation_internationalization(apps, schema_editor):
    model = apps.get_model('violation', 'TypeViolation')
    for row in model.objects.all():
        if row.info.all().count() == 0:
            TypeViolationInternationalization.objects.create(row.id, 'pt', row.name, row.description, row.action)


class Migration(migrations.Migration):
    dependencies = [
        ('violation', '0005_auto_20160408_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='TypeViolationInternationalization',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('language', models.CharField(max_length=2, default='pt', choices=[('pt', 'Português'), ('en', 'English'), ('es', 'Español')], verbose_name='Idioma')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('description', models.TextField(help_text='Insira uma descrição para o tipo de violação.', verbose_name='Descrição')),
                ('action', models.TextField(blank=True, null=True, help_text='Insira a ação a ser tomada.', verbose_name='Ação')),
                ('date_joined', models.DateTimeField(auto_now_add=True, help_text='Data de cadastro', verbose_name='Data de cadastro')),
                ('typeviolation', models.ForeignKey(to='violation.TypeViolation', related_name='info', verbose_name='Tipo de violação')),
            ],
        ),
        migrations.RunPython(
            code=populate_typeviolation_internationalization,
            atomic=True
        ),
    ]
