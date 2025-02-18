from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    
    search_fields = ["user__username", "name", "category__name", "price"]
    list_display = ["user__username", "name", "price", "active"]
    list_filter = ["price", "active"]
    readonly_fields = ["show_image", "updated_at", "created_at"]
    fieldsets = (
        (None, {"fields": ("category", "user")}),
        ("Image", {"fields": ( "image", "show_image")}),
        ("Extra", {"fields": ("name", "price", "description", "slug", "active","quantities", "tags", "views")}),
        ("Date", {"fields": ("created_at", "updated_at")}),
    )

    def show_image(self, obj):
        return format_html(f"<img src=\"{obj.image.url}\" width=\"300\" />")

    show_image.short_description = "Current Image"


class ItemInline(admin.StackedInline):
    model = Item
    extra = 0
    

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    
    list_filter = ["name"]
    search_fields = ["name"]
    inlines = [ItemInline]
