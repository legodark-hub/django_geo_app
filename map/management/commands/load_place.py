import os
import requests
from urllib.parse import urlparse

from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from map.models import Place, Image


class Command(BaseCommand):
    help = 'Загружает данные из JSON в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('json_url', type=str, help='Ссылка на JSON файл')

    def handle(self, *args, **options):
        json_url = options['json_url']

        try:
            response = requests.get(json_url)
            response.raise_for_status() 
            data = response.json()

            place, created = Place.objects.get_or_create(
                title=data['title'],
                defaults={
                    'description_short': data.get('description_short', ''),
                    'description_long': data.get('description_long', ''),
                    'lng': data['coordinates']['lng'],
                    'lat': data['coordinates']['lat'],
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Место успешно добавлено: "{place.title}"'))
            else:
                self.stdout.write(self.style.WARNING(f'Место с названием"{place.title}" уже существует. Обновление...'))
                place.description_short = data.get('description_short', '')
                place.description_long = data.get('description_long', '')
                place.lng = data['coordinates']['lng']
                place.lat = data['coordinates']['lat']
                place.save()


            if not created:
                place.images.all().delete()

            for img_url in data.get('imgs', []):
                try:
                    img_response = requests.get(img_url)
                    img_response.raise_for_status()

                    parsed_url = urlparse(img_url)
                    img_name = os.path.basename(parsed_url.path)

                    Image.objects.create(
                        place=place,
                        image=ContentFile(img_response.content, name=img_name)
                    )
                    self.stdout.write(self.style.SUCCESS(f'  - Изображение загружено: {img_name}'))

                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f'  - Не удалось загрузить изображение{img_url}: {e}'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Не удалось получить данные из{json_url}: {e}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Неправильный формат JSON:{e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Произошла ошибка: {e}'))
