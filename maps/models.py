from django.db import models
from mapbox_location_field.models import LocationField, AddressAutoHiddenField


class Location(models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)

    description = models.TextField(null=False, blank=False)

    created_at = models.DateTimeField(auto_now_add=True)

    free = models.BooleanField(blank=False, null=False, default=False)

    coordinates = LocationField(
        map_attrs={
            "style": "mapbox://styles/mapbox/streets-v11",
            "center": (35.921637, -79.077887),
            "zoom": 5,
            "rotate": True,
            "navigation_buttons": True,
            "track_location_button": True,
            "id": "map",
        }
    )  # this gets reversed when delivered with the api for some reason?

    address = AddressAutoHiddenField(map_id="map")

    class LocationTypeChoices(models.TextChoices):
        PARK = "PA", ("Dog Park")
        RESTAURANT = "RE", ("Restaurant")
        VET = "VE", ("Veterinarian")
        TRAIL = "TR", ("Trail")
        HOUSE = "HO", ("House")

    location_type = models.CharField(
        max_length=2,
        choices=LocationTypeChoices.choices,
        default=LocationTypeChoices.PARK,
        null=True,
        blank=True,
    )

    def __str__(self):
        def loc_type():
            if self.location_type == "HO":
                return "House"
            elif self.location_type == "PA":
                return "Park"
            elif self.location_type == "RE":
                return "Restaurant"
            elif self.location_type == "VE":
                return "Veterinarian"
            return "Trail"

        return f"{loc_type()} called '{self.name[:50]}'"