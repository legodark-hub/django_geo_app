from django.db import models


class Place(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description_short = models.TextField(verbose_name="Краткое описание")
    description_long = models.TextField(verbose_name="Полное описание")
    lng = models.FloatField(verbose_name="Долгота")
    lat = models.FloatField(verbose_name="Широта")

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        Place, on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Место"
    )
    image = models.ImageField(verbose_name="Картинка")

    def __str__(self):
        return f'{self.id} {self.place.title}'
