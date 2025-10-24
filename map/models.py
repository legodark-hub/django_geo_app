from django.db import models
from django.utils.html import format_html


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = models.TextField(verbose_name="Полное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Место"
    )
    image = models.ImageField(verbose_name="Картинка")
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['position']

    def get_preview(self):
        return format_html('<img src="{}" height="200" />', self.image.url)

    get_preview.short_description = 'Предпросмотр'

    def __str__(self):
        return f'{self.id} {self.place.title}'