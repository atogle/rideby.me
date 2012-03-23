from django.contrib.gis.db import models


class Stop(models.Model):
    id = models.TextField(primary_key=True, db_column="stop_id")
    name = models.TextField(db_column="stop_name")

    geom = models.PointField(db_column="the_geom")
    objects = models.GeoManager()

    class Meta:
        db_table = "gtfs_stops"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name


class StopTime(models.Model):
    id = models.PositiveIntegerField(
        primary_key=True, db_column='stop_time_id')
    stop = models.ForeignKey("Stop")
    trip = models.ForeignKey("Trip")
    departure_time = models.TextField()
    departure_seconds = models.PositiveIntegerField(
      db_column="departure_time_seconds")

    class Meta:
        db_table = "gtfs_stop_times"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return "%s, %s" % (self.stop.name, self.departure_time)


class Trip(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column='trip_id')
    headsign = models.TextField(db_column='trip_headsign')
    direction_id = models.PositiveIntegerField()
    shape = models.ForeignKey("Shape")
    route = models.ForeignKey("Route")

    class Meta:
        db_table = "gtfs_trips"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.headsign


class Route(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column='route_id')
    short_name = models.TextField(db_column='route_short_name')
    long_name = models.TextField(db_column='route_long_name')

    class Meta:
        db_table = "gtfs_routes"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.short_name


class Shape(models.Model):
    id = models.PositiveIntegerField(primary_key=True, db_column="shape_id")
    geom = models.PointField(db_column="the_geom")
    objects = models.GeoManager()

    class Meta:
        db_table = "gtfs_shape_geoms"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.id
