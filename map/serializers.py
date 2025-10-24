from rest_framework import serializers
from .models import Place, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class PlaceSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    coordinates = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = ['id', 'title', 'images', 'description_short', 'description_long', 'coordinates']

    def get_coordinates(self, obj):
        return {
            "lng": obj.lng,
            "lat": obj.lat
        }
