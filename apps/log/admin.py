from django.contrib import admin
from apps.log.models import Log


class LogAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'description', 'createdAt',)
    list_display_links = list_display
    list_per_page = 30
    list_filter = ('createdAt',)
    search_fields = ('identifier', 'description',)


admin.site.register(Log, LogAdmin)
