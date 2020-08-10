from django.conf.urls import patterns, url

from apps.api.v1.views import Feedback

urlpatterns = patterns('apps.api.v1.views',

                       url(r'^themes/$', 'theme'),
                       url(r'^themes/(?P<theme_id>[\w-]+)/$', 'theme_getone'),

                       url(r'^protection_network/types/$', 'typeprotectionnetwork'),
                       url(r'^protection_network/types/(?P<typeprotectionnetwork_id>[\w-]+)/$',
                           'typeprotectionnetwork_getone'),
                       url(r'^protection_network/$', 'protectionnetwork'),

                       url(r'^protection_network/(?P<protectionnetwork_id>[\w-]+)/$',
                           'protectionnetwork_getone'),

                       url(r'^protection_network/state/(?P<initials>[\w-]+)/$',
                           'protectionnetwork_getforstate'),
                       url(r'^protection_network/theme/(?P<theme_id>[\w-]+)/$',
                           'protectionnetwork_getfortheme'),
                       url(r'^protection_network/type/(?P<type_id>[\w-]+)/$',
                           'protectionnetwork_getfortype'),
                       url(r'^protection_network/state/(?P<initials>[\w-]+)/theme/(?P<theme_id>[\w-]+)/$',
                           'protectionnetwork_getforstateandtheme'),

                       url(
                           r'^protection_network/type/(?P<type_id>[\w-]+)/position/(?P<lat>-\d+\.\d+),(?P<long>-\d+\.\d+)/$',
                           'protectionnetwork_getfortypeandcoordenates'),
                       url(
                           r'^protection_network/theme/(?P<theme_id>[\w-]+)/position/(?P<lat>-\d+\.\d+),(?P<long>-\d+\.\d+)/radius/(?P<distance>[\w-]+)/$',
                           'protectionnetwork_getforthemeandcoordenates'),

                       url(r'^violation_type/$', 'typeviolation'),
                       url(r'^violation_type/(?P<typeviolation_id>[\w-]+)/$', 'typeviolation_getone'),
                       url(r'^violation_type/theme/(?P<theme_id>[\w-]+)/$', 'typeviolation_getfortheme'),
                       url(r'^violation_type/type/(?P<typeprotectionnetwork_id>[\w-]+)/$',
                           'typeviolation_getfortype'),
                       url(r'^violation_type/category/(?P<category>[\w-]+)/$',
                           'typeviolation_getforcategory'),

                       url(r'^feedback/$', Feedback.as_view()),

                       url(
                           r'^protection_network/name/(?P<name>[\w|\W]+)/position/(?P<lat>-\d+\.\d+),(?P<long>-\d+\.\d+)/$',
                           'protectionnetwork_getbynameandcoordenates'),

                       url(r'^protection_network/name/(?P<name>[\w|\W]+)/$',
                           'protectionnetwork_getbyname'),

                       )
