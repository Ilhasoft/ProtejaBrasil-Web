from django.db import models


class ImportManager(models.Manager):
    def add_import(self, file):
        item = self.model(
            file=file,
        )
        item.save(using=self._db)
        return item


class Import(models.Model):
    file = models.FileField(upload_to='importation')
    date_joined = models.DateTimeField(verbose_name='Data de cadastro', help_text='Data de cadastro',
                                       auto_now_add=True, editable=False)
    objects = ImportManager()
