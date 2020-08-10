from django.contrib import admin
from apps.feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('type', 'name', 'email', 'platform', 'version', 'createdAt',)
    list_display_links = list_display
    readonly_fields = ('createdAt',)
    list_filter = ('type', 'createdAt', 'platform', )
    list_per_page = 30
    search_fields = ('name', 'email', 'message',)


admin.site.register(Feedback, FeedbackAdmin)
