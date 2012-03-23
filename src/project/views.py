from django.contrib.gis.geos import Point
from django.http import HttpResponse
from project.models import Stop, StopTime
from vectorformats.Formats import Django, GeoJSON


def stops(request):
    lon = float(request.GET.get('lon', 0))
    lat = float(request.GET.get('lat', 0))
    radius = float(request.GET.get('radius', 800))

    stops = get_stops(lon, lat, radius)
    geojson = queryset_to_geojson(stops)

    return HttpResponse(geojson, mimetype='application/json')


def routes(request):
    lon = float(request.GET.get('lon', 0))
    lat = float(request.GET.get('lat', 0))
    radius = float(request.GET.get('radius', 800))

    stops = get_stops(lon, lat, radius)
    route_shortnames = StopTime.objects.filter(
        stop__in=stops).values('trip__route__short_name').distinct()

    # return HttpResponse(geojson, mimetype='application/json')
    return HttpResponse(
        [obj['trip__route__short_name'] for obj in route_shortnames])


def queryset_to_geojson(qs):
    django_format = Django.Django(geodjango='geom', properties=['id', 'name'])
    geojson_format = GeoJSON.GeoJSON()
    return geojson_format.encode(django_format.decode(qs))


def get_stops(lon, lat, radius):
    center = Point(lon, lat)
    return Stop.objects.filter(geom__distance_lte=(center, radius))
