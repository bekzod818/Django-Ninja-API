from django.shortcuts import get_object_or_404
from ninja_extra.ordering import ordering, Ordering
from ninja_extra.searching import searching, Searching
from ninja_extra.throttling import UserRateThrottle
from ninja_extra import NinjaExtraAPI, api_controller, route, permissions, throttle, paginate
from .models import Location, Device
from ninja_jwt.authentication import JWTAuth
from .schemas import (
    LocationSchema,
    DeviceSchema,
    DeviceCreateSchema,
    DeviceUpdateSchema,
    Error,
    DeviceLocationPatch,
)
from ninja_jwt.controller import NinjaJWTDefaultController


app = NinjaExtraAPI(version="1.0.0")

@api_controller("/devices", tags=["Devices"], permissions=[permissions.IsAuthenticatedOrReadOnly])
class DeviceController:
    @route.get("/", response=list[DeviceSchema], permissions=[])
    @ordering(Ordering, ordering_fields=['id', 'location'])
    @searching(Searching, search_fields=['=name', '=location__name'])
    @throttle
    def get_devices(self):
        return Device.objects.all()


    @route.post("/", response={200: DeviceSchema, 404: Error})
    @throttle(UserRateThrottle)
    def create_device(self, device: DeviceCreateSchema):
        if device.location_id:
            # we have a location_id in the body
            location_exists = Location.objects.filter(id=device.location_id).exists()
            if not location_exists:
                return 404, {"message": "Location not found!"}

        device_data = device.model_dump()
        device_model = Device.objects.create(**device_data)
        return device_model


    @route.get("/{slug}", response=DeviceSchema)
    def get_device_detail(request, slug: str):
        device = get_object_or_404(Device, slug=slug)
        return device


    @route.put("/{slug}", response=DeviceSchema, auth=JWTAuth())
    def update_device(request, slug: str, device: DeviceUpdateSchema):
        device_model = get_object_or_404(Device, slug=slug)
        for attr, value in device.dict(
            exclude_unset=True
        ).items():  # Partial updates -> To allow the user to make partial updates, use payload.dict(exclude_unset=True).items(). This ensures that only the specified fields get updated.
            if attr == "location_id":
                location = get_object_or_404(Location, id=value)
                device_model.location = location
            else:
                setattr(device_model, attr, value)
        device_model.save()
        return device_model


    @route.delete("/{slug}", auth=JWTAuth())
    def delete_device(request, slug: str):
        device = get_object_or_404(Device, slug=slug)
        device.delete()
        return {"deleted": True}


    @route.post("/{device_slug}/set-location", response=DeviceSchema)
    def update_device_location(request, device_slug: str, location: DeviceLocationPatch):
        device = get_object_or_404(Device, slug=device_slug)
        if location.location_id:
            location = get_object_or_404(Location, id=location.location_id)
            device.location = location
        else:
            device.location = None

        device.save()
        return device


@api_controller("/locations", tags=["Locations"], permissions=[])
class LocationController:
    """
    If you use the paginate decorator and the ordering decorator together, the paginate decorator should be above the ordering decorator because first the data are sorted and then the data are paginated, for example:
    """
    @route.get("/", response=list[LocationSchema])
    # @paginate()
    @ordering(Ordering, ordering_fields=['name'])
    # If you use the paginate decorator, the ordering decorator and the searching decorator together, the paginate decorator should be above the ordering decorator and the ordering decorator should be above the searching decorator because first the data is filtered, then the data is sorted and then paginated:, for example:
    @searching(Searching, search_fields=['name'])
    def get_locations(self):
        return Location.objects.all()

app.register_controllers(
    DeviceController,
    LocationController,
    NinjaJWTDefaultController,
)
