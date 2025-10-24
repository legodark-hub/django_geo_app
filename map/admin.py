from django.contrib import admin
from .models import Place, Image
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_preview',)


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('get_preview',)


@admin.register(Place)
class PlaceAdmin(SortableAdminMixin, admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title', 'position',)
