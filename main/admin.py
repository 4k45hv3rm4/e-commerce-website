from django.contrib import admin
from django.apps import apps
from . import models
from django.utils.html import format_html
# class ListAdminMixin(object):
#     def __init__(self, model, admin_site):
#         self.list_display = [field.name for field in model._meta.fields]
#         super(ListAdminMixin, self).__init__(model, admin_site)
#
#
# models = apps.get_models()
# print(models, 'model')
# for model in models:
#     admin_class = type('AdminClass', (ListAdminMixin, admin.ModelAdmin), {})
#     try:
#         admin.site.register(model, admin_class)
#     except admin.sites.AlreadyRegistered:
#         pass


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'in_stock', 'price')
    list_filter = ('active', 'in_stock', 'date_updated')
    list_editable = ('in_stock',)
    search_fields = ('name',)
    autocomplete_fields = ('tags', )
    prepopulated_fields = {"slug": ('name', )}


admin.site.register(models.Product, ProductAdmin)


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    list_filter = ('active',)
    search_fields = ('name', )
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(models.ProductTag, ProductTagAdmin)

class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag', 'product_name')
    readonly_fields = ('thumbnail',)
    search_fields = ('product_name', )

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html('<img src="%s" />' % obj.thumbnail.url)
        return "-"
    thumbnail_tag.short_description = "Thumbnail"

    def product_name(self, obj):
        return obj.product.name

admin.site.register(models.ProductImage, ProductImageAdmin)

from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

@admin.register(models.User)

class UserAdmin(DjangoUserAdmin):
    fieldsets= (
        (None, {'fields': ('email', 'password')}),
        (
            'Personal Info',
            {
                "fields": ('first_name', 'last_name')
            },
        ),
        ("Permissions",
         {
             'fields': ('is_active', 'is_staff', 'is_superuser',
                        'groups', 'user_permissions')
          },
         ),
        (
            "Important dates", {'fields':('last_login', 'date_joined')}
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide', ),
                'fields': ('email', 'password1', 'password2'),
            }
        )
    )
    list_display = (
        'email',
        'first_name',
        'last_name',
        'is_staff'
    )
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
