from django.db import models


class UF(models.Model):
    initials = models.CharField(verbose_name='Sigla', help_text='Insira a sigla do estado', max_length=3,
                                unique=True, )
    title = models.CharField(verbose_name='Nome do estado', help_text='Insira o título do estado', max_length=100, )

    def __str__(self):
        return '{0}'.format(self.title)

    class Meta:
        verbose_name = 'Estado'
        verbose_name_plural = 'Estados'
