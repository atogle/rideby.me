from django.contrib.gis.geos import Point
from django.http import HttpResponse
from project.models import Stop
from vectorformats.Formats import Django, GeoJSON


def stops(request):
    django_format = Django.Django(geodjango='geom', properties=['id', 'name'])
    geojson_format = GeoJSON.GeoJSON()

    lat = float(request.GET.get('lat', 0))
    lon = float(request.GET.get('lon', 0))
    radius = float(request.GET.get('radius', 800))

    center = Point(lon, lat)
    result = Stop.objects.filter(geom__distance_lte=(center, radius))
    geojson = geojson_format.encode(django_format.decode(result))

    return HttpResponse(geojson, mimetype='application/json')
