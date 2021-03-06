from django.contrib import admin
from shop.models import Phone, CartCompanion, Article, SiteField, Comment, Order


class CartInline(admin.TabularInline):
    model = CartCompanion.cart.through
    extra = 1


class OrderInline(admin.TabularInline):
    model = Order.phones.through
    extra = 0


class ArticleInline(admin.TabularInline):
    model = Article.phones.through


#
# class SiteFieldInline(admin.TabularInline):
#     model = SiteField.dropdown_fields.through


def make_visible(model, request, queryset):
    queryset.update(visible_status="v")


make_visible.short_description = "Make objects visible"


def make_invisible(model, request, queryset):
    queryset.update(visible_status="i")


make_invisible.short_description = "Make objects invisible"


def print_id(model, request, queryset):
    for obj in queryset:
        print(f"{obj.name}: {obj.id}")


print_id.short_description = "Print ID shortcut"


class PhoneAdmin(admin.ModelAdmin):
    list_display = ["name", "visible_status", "type"]
    actions = [make_visible, make_invisible, print_id]


admin.site.register(Phone, PhoneAdmin)


class CartCompanionAdmin(admin.ModelAdmin):
    inlines = [
        CartInline
    ]
    list_display = ["user"]
    exclude = ["cart"]


admin.site.register(CartCompanion, CartCompanionAdmin)


def print_article_id(model, request, queryset):
    for obj in queryset:
        print(f"{obj.title}: {obj.id}")


print_article_id.short_description = "Print ID shortcut"


class ArticleAdmin(admin.ModelAdmin):
    actions = [make_visible, make_invisible, print_article_id]
    list_display = [
        "title",
        "visible_status"
    ]
    inlines = [
        ArticleInline
    ]
    exclude = [
        "phones"
    ]


admin.site.register(Article, ArticleAdmin)


class SiteFieldAdmin(admin.ModelAdmin):
    actions = [make_visible, make_invisible]
    list_display = ["name", "visible_status"]


admin.site.register(SiteField, SiteFieldAdmin)


class CommentAdmin(admin.ModelAdmin):
    actions = [make_visible, make_invisible]
    list_display = ["author", "ratio", "visible_status"]


admin.site.register(Comment, CommentAdmin)


class OrderAdmin(admin.ModelAdmin):
    actions = [make_visible, make_invisible]
    list_display = ["user", "date"]
    inlines = [
        OrderInline
    ]
    exclude = [
        "phones"
    ]


admin.site.register(Order, OrderAdmin)

