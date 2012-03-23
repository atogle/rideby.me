from django.contrib.gis.geos import Point
from django.http import HttpResponse
from project.models import Stop, Route
from vectorformats.Formats import Django, GeoJSON


def stops(request):
    lon = float(request.GET.get('lon', 0))
    lat = float(request.GET.get('lat', 0))
    radius = float(request.GET.get('radius', 800))

    center = Point(lon, lat)
    stops = Stop.objects.filter(geom__distance_lte=(center, radius))
    geojson = queryset_to_geojson(stops, ['id', 'name'])

    return HttpResponse(geojson, mimetype='application/json')


def routes(request):
    lon = float(request.GET.get('lon', 0))
    lat = float(request.GET.get('lat', 0))
    radius = float(request.GET.get('radius', 800))

    center = Point(lon, lat)
    routes = Route.objects.filter(
        stop__geom__distance_lte=(center, radius)).distinct()
    geojson = queryset_to_geojson(routes, ['id', 'short_name', 'long_name'])

    return HttpResponse(geojson, mimetype='application/json')


def queryset_to_geojson(qs, props):
    django_format = Django.Django(geodjango='geom', properties=props)
    geojson_format = GeoJSON.GeoJSON()
    return geojson_format.encode(django_format.decode(qs))
