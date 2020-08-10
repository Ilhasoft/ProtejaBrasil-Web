from django.contrib import admin
from apps.authorization.models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('application', 'token', 'is_active',)
    list_display_links = ('application', 'token',)
    search_fields = ('application', 'token',)
    list_per_page = 30
    readonly_fields = ('token',)
    list_editable = ('is_active',)


admin.site.register(Token, TokenAdmin)
