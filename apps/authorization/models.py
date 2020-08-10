from django.db import models
from apps.utils.codgenarator import generator


class Token(models.Model):
    application = models.CharField(verbose_name='Aplicação',
                                   help_text='Insira o nome da aplicação que usará o token gerado.', max_length=255, )
    token = models.CharField(verbose_name='Token', help_text='Token de autorização', unique=True, max_length=30, )
    is_active = models.BooleanField(verbose_name='Ativo',
                                    help_text='Selecione se deseja permitir que esse aplicativo consulte a API',
                                    default=True, )

    def __str__(self):
        return '{0}'.format(self.application)

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'

    def save(self, *args, **kwargs):
        if not self.id:
            self.token = generator(30)
        super(Token, self).save(*args, **kwargs)
