from django.contrib import admin
from django.utils.html import format_html

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    search_fields = ["user__username", "user__email", "pk"]
    readonly_fields = ["show_flag"]
    list_filter = ["country"]
    list_display = ["user__username", "user__email", "country", "show_flag"]

    @admin.display(description="Flag")
    def show_flag(self, obj):
        return format_html(f"<img src=\"{obj.country.flag}\" />")