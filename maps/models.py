from django.db import models
from mapbox_location_field.spatial.models import SpatialLocationField


class Location(models.Model):
    location = SpatialLocationField(
        map_attrs={
            "style": "mapbox://styles/mapbox/streets-v11",
            "center": (-80.793457, 35.782169),
            "zoom": 5,
        }
    )
