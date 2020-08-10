from django.contrib import admin
from apps.theme.models import Theme, ThemeInternationalization


class ThemeInternationalizationInline(admin.StackedInline):
    model = ThemeInternationalization
    min_num = 1
    max_num = 3
    extra = 0


class ThemeAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/jscolor.js', 'js/setClass.js')

    inlines = [ThemeInternationalizationInline, ]
    list_display = ('title', 'order',)
    list_display_links = ('title',)
    list_editable = ('order',)
    search_fields = ('title', 'description',)
    list_per_page = 30
    ordering = ('order',)


admin.site.register(Theme, ThemeAdmin)
