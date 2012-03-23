from django.contrib.gis.db import models


class Stop(models.Model):
    id = models.TextField(primary_key=True, db_column="stop_id")
    name = models.TextField(db_column="stop_name")
    routes = models.ManyToManyField('Route', through='RouteStops')

    geom = models.PointField(db_column="the_geom")
    objects = models.GeoManager()

    class Meta:
        db_table = "gtfs_stops"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name


class Route(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column='route_id')
    short_name = models.TextField(db_column='route_short_name')
    long_name = models.TextField(db_column='route_long_name')
    geom = models.LineStringField(db_column="the_geom")
    objects = models.GeoManager()

    class Meta:
        db_table = "gtfs_routes"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.short_name


class RouteStops(models.Model):
    route = models.ForeignKey(Route)
    stop = models.ForeignKey(Stop)

    class Meta:
        db_table = "route_stops"
        managed = False
