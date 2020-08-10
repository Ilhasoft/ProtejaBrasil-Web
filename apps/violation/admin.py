from django.contrib import admin
from apps.violation.models import TypeViolation, TypeProtectionNetwork, CategoryTypeViolation, TypeViolationInternationalization


class TypeProtectionNetworkInline(admin.StackedInline):
    model = TypeProtectionNetwork
    extra = 0


class CategoryTypeViolationInline(admin.StackedInline):
    model = CategoryTypeViolation
    extra = 0


class TypeViolationInternationalizationInline(admin.StackedInline):
    model = TypeViolationInternationalization
    min_num = 1
    max_num = 3
    extra = 0


class TypeViolationAdmin(admin.ModelAdmin):
    inlines = [TypeViolationInternationalizationInline, TypeProtectionNetworkInline, CategoryTypeViolationInline, ]
    list_display = ('name', 'theme',)
    list_display_links = list_display
    list_per_page = 30
    list_filter = ('theme',)
    search_fields = ('name', 'description', 'action', 'info__name', 'info__description',)


admin.site.register(TypeViolation, TypeViolationAdmin)
