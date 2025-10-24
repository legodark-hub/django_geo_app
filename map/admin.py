from django.contrib import admin
from django import forms
from .models import Place, Image
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class PlaceAdminForm(forms.ModelForm):
    description_short = forms.CharField(label='Краткое описание', widget=CKEditorUploadingWidget())
    description_long = forms.CharField(label='Полное описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Place
        fields = '__all__'


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
    form = PlaceAdminForm
    list_display = ('title', 'position',)
