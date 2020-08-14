from django.contrib import admin
from shop.models import Phone


def make_visible(model, request, queryset):
    queryset.update(visible_status="v")


make_visible.short_description = "Make objects visible"


def make_invisible(model, request, queryset):
    queryset.update(visible_status="i")


make_invisible.short_description = "Make objects invisible"


class PhoneAdmin(admin.ModelAdmin):
    list_display = ["name", "visible_status"]
    actions = [make_visible, make_invisible]


admin.site.register(Phone, PhoneAdmin)
