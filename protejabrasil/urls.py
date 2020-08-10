from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                           'document_root': settings.MEDIA_ROOT}),
                       (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
                           'document_root': settings.STATIC_ROOT}),

                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api/v1/docs/', include('rest_framework_swagger.urls')),
                       url(r'^api/v1/', include('apps.api.v1.urls')),
                       url(r'^api/v2/', include('apps.api.v2.urls')),
                       url(r'^', include('apps.application.urls'), name='application'),

                       )
