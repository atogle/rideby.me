from django.contrib.gis.db import models


class Stop(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    id = models.PositiveIntegerField(primary_key=True, db_column="stop_id")
    name = models.TextField(db_column="stop_name")

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    geom = models.PointField(db_column="the_geom")
    objects = models.GeoManager()

    class Meta:
        db_table = "gtfs_stops"
        managed = False

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
