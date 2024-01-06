from .models import Location, Device
from ninja import ModelSchema


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ("id", "name")


class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None

    class Meta:
        model = Device
        fields = ("id", "name", "slug", "location")
