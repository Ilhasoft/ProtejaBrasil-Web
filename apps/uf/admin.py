from django.contrib import admin
from apps.uf.models import UF


class UFAdmin(admin.ModelAdmin):
    list_display = ('title', 'initials',)
    list_display_links = list_display
    list_per_page = 30
    search_fields = ('title', 'initials',)


admin.site.register(UF, UFAdmin)
