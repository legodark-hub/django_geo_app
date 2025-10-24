from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from .models import Place
from .serializers import PlaceSerializer


def map_view(request):
    return render(request, 'index.html')


class PlaceViewSet(ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer