from django.db import models


class LogManager(models.Manager):
    def create_log(self, identifier, description):
        item = self.model(
            identifier=identifier,
            description=description
        )
        item.save(using=self._db)
        return item


class Log(models.Model):
    identifier = models.CharField(verbose_name='Local da aplicação', max_length=255, )
    description = models.TextField(verbose_name='Descrição', null=True, )
    createdAt = models.DateTimeField(verbose_name='Data de cadastro', auto_now_add=True, blank=True, )
    objects = LogManager()

    def __str__(self):
        return '{0}'.format(self.identifier)

    class Meta:
        verbose_name = 'Log'
        verbose_name_plural = 'Logs'
