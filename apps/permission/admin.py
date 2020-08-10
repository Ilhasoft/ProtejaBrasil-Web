from django.contrib import admin
from apps.permission.models import Module, Permission


class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'alias',)
    list_display_links = list_display
    list_per_page = 30
    search_fields = ('name',)


class PermissionAdmin(admin.ModelAdmin):
    list_display = ('name', 'module', 'alias',)
    list_display_links = list_display
    list_per_page = 30
    search_fields = ('name', 'alias',)
    list_filter = ('module',)


admin.site.register(Module, ModuleAdmin)
admin.site.register(Permission, PermissionAdmin)
