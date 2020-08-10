# -*- coding: utf-8 -*-

__author__ = u'teehamaral'

from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       url(r'^$', 'apps.application.views.login', name='app_login'),

                       url(r'^importar-redes-de-protecao/$', 'apps.application.views.import_protectionnetworks', name='app_import_protectionnetworks'),

                       url(r'^esqueceu-a-senha/$', 'apps.application.views.forgotpassword', name='app_forgotpassword'),
                       url(r'^dashboard/$', 'apps.application.views.dashboard', name='app_dashboard'),

                       url(r'^usuarios/$', 'apps.application.views.users_list', name='app_userslist'),
                       url(r'^usuarios/adicionar/$', 'apps.application.views.users_add', name='app_usersadd'),
                       url(r'^usuarios/editar/(?P<id>[\w-]+)/$', 'apps.application.views.users_edit', name='app_usersedit'),
                       url(r'^usuarios/excluir/(?P<id>[\w-]+)/$', 'apps.application.views.users_del', name='app_usersdel'),
                       url(r'^usuarios/alterar-senha/(?P<id>[\w-]+)/$', 'apps.application.views.users_change_password', name='app_userschangepassword'),

                       url(r'^redes-de-protecao/tipos/$', 'apps.application.views.typesprotectionnetwork_list', name='app_typesprotectionnetworklist'),
                       url(r'^redes-de-protecao/tipos/adicionar/$', 'apps.application.views.typesprotectionnetwork_add', name='app_typesprotectionnetworkadd'),
                       url(r'^redes-de-protecao/tipos/editar/(?P<id>[\w-]+)/$', 'apps.application.views.typesprotectionnetwork_edit', name='app_typesprotectionnetworkedit'),
                       url(r'^redes-de-protecao/tipos/excluir/(?P<id>[\w-]+)/$', 'apps.application.views.typesprotectionnetwork_del', name='app_typesprotectionnetworkdel'),

                       url(r'^redes-de-protecao/$', 'apps.application.views.protectionnetwork_list', name='app_protectionnetworklist'),
                       url(r'^redes-de-protecao/adicionar/$', 'apps.application.views.protectionnetwork_add', name='app_protectionnetworkadd'),
                       url(r'^redes-de-protecao/editar/(?P<id>[\w-]+)/$', 'apps.application.views.protectionnetwork_edit', name='app_protectionnetworkedit'),
                       url(r'^redes-de-protecao/excluir/(?P<id>[\w-]+)/$', 'apps.application.views.protectionnetwork_del', name='app_protectionnetworkdel'),

                       url(r'^tipos-de-violacao/$', 'apps.application.views.typesviolation_list', name='app_typesviolationlist'),
                       url(r'^tipos-de-violacao/adicionar/$', 'apps.application.views.typesviolation_add', name='app_typesviolationadd'),
                       url(r'^tipos-de-violacao/editar/(?P<id>[\w-]+)/$', 'apps.application.views.typesviolation_edit', name='app_typesviolationedit'),
                       url(r'^tipos-de-violacao/excluir/(?P<id>[\w-]+)/$', 'apps.application.views.typesviolation_del', name='app_typesviolationedel'),

                       url(r'^feedback/$', 'apps.application.views.feedback', name='app_feedback'),
                       url(r'^feedback/resolvido/(?P<id>[\w-]+)/$', 'apps.application.views.feedback_as_resolved', name='app_feedback_as_resolved'),

                       url(r'^sair/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='app_logout'),
                       )
