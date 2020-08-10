from django.db import models


class Module(models.Model):
    name = models.CharField(verbose_name='Nome',
                            help_text='Nome do módulo. Ex.: Usuário, Denúncia, Rede de proteção', max_length=255, )
    alias = models.CharField(verbose_name='Apelido',
                             help_text='Apelido do módulo (escrito em letras minúsculas e sem acentuação. Ex.: usuario, denuncia, redes_de_protecao.)',
                             max_length=255, )

    def __str__(self):
        return '{0}'.format(self.name)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'


class Permission(models.Model):
    name = models.CharField(verbose_name='Nome',
                            help_text='Nome da permissão. Ex.: Adicionar usuário, Editar usuário', max_length=255, )
    module = models.ForeignKey(Module, verbose_name='Módulo',
                               help_text='Selecione o módulo que a permissão pertence', )
    alias = models.CharField(verbose_name='Apelido',
                             help_text='Apelido da permissão (escrito em letras minúsculas e sem acentuação. Ex.: add_usuario, edit_denuncia, add_redes_de_protecao.)',
                             max_length=255, )

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.module)

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'
