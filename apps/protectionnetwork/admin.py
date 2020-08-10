from django.contrib import admin
from apps.protectionnetwork.models import Type, ThemeProtectionNetwork, OperatingDaysProtectionNetwork, \
    ProtectionNetwork, TypeInternationalization, ProtectionNetworkInternationalization


class ThemeProtectionNetworkInline(admin.StackedInline):
    model = ThemeProtectionNetwork
    extra = 0


class OperatingDaysProtectionNetworkInline(admin.StackedInline):
    model = OperatingDaysProtectionNetwork
    extra = 0
    max_num = 7


class TypeInternacionalizationInline(admin.StackedInline):
    model = TypeInternationalization
    extra = 0
    max_num = 3
    min_num = 1


class ProtectionNetworkInternationalizationInline(admin.StackedInline):
    model = ProtectionNetworkInternationalization
    min_num = 1
    max_num = 3
    extra = 0


class ProtectionNetworkAdmin(admin.ModelAdmin):
    inlines = [ProtectionNetworkInternationalizationInline, ThemeProtectionNetworkInline, OperatingDaysProtectionNetworkInline, ]
    list_display = ('name', 'type', 'city', 'state',)
    list_display_links = list_display
    list_per_page = 30
    list_filter = ('type', 'state',)
    search_fields = ('name', 'city', 'info__name', 'state__initials', 'state__title',)


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [TypeInternacionalizationInline, ]
    list_display_links = list_display
    search_fields = ('name',)
    list_per_page = 30


admin.site.register(Type, TypeAdmin)
admin.site.register(ProtectionNetwork, ProtectionNetworkAdmin)
