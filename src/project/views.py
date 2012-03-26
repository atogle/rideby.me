from django.contrib.gis.geos import Point
from django.http import HttpResponse
from project.models import Stop, Route
from vectorformats.Formats import Django, GeoJSON


def stops(request):
    radius = float(request.GET.get('radius', 800))
    point = get_point(request)

    return HttpResponse(get_stop_geojson(point, radius),
        mimetype='application/json')


def routes(request):
    radius = float(request.GET.get('radius', 800))
    point = get_point(request)

    return HttpResponse(get_route_geojson(point, radius),
        mimetype='application/json')


def transit(request):
    radius = float(request.GET.get('radius', 800))
    point = get_point(request)

    geojson = """
        {
          "center": {"lat":%f, "lon":%f, "radius":%d},
          "stops": %s,
          "routes": %s
        } """ % (
            point.y, point.x, radius,
            get_stop_geojson(point, radius),
            get_route_geojson(point, radius)
        )

    return HttpResponse(geojson, mimetype='application/json')


def queryset_to_geojson(qs, props):
    django_format = Django.Django(geodjango='geom', properties=props)
    geojson_format = GeoJSON.GeoJSON()
    return geojson_format.encode(django_format.decode(qs))


def get_point(request):
    lon = float(request.GET.get('lon', 0))
    lat = float(request.GET.get('lat', 0))

    return Point(lon, lat)


def get_stop_geojson(point, radius):
    stops = Stop.objects.filter(geom__distance_lte=(point, radius))
    return queryset_to_geojson(stops, ['id', 'name'])


def get_route_geojson(point, radius):
    routes = Route.objects.filter(
        stop__geom__distance_lte=(point, radius)).distinct()
    return queryset_to_geojson(routes, ['id', 'short_name', 'long_name'])
