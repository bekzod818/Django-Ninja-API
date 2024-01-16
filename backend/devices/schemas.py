from .models import Location, Device
from ninja import ModelSchema, Schema


class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ("id", "name")


class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None

    class Meta:
        model = Device
        fields = ("id", "name", "slug", "location")


class DeviceCreateSchema(Schema):
    name: str
    location_id: int | None = None


class Error(Schema):
    message: str


class DeviceLocationPatch(Schema):
    location_id: int | None = None


class DeviceUpdateSchema(DeviceCreateSchema):
    name: str | None = None

    class Config:
        """
        Enforcing strict field validation
        By default, any provided fields that don't exist in the schema will be silently ignored. To raise an error for these invalid fields, you can set extra = "forbid" in the schema's Config class. For example:
        """

        extra = "forbid"
