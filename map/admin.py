from django.contrib import admin
from .models import Place, Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'get_preview',)


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    readonly_fields = ('get_preview',)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline]
    list_display = ('title',)