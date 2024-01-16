from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from .models import Location, Device
from .schemas import (
    LocationSchema,
    DeviceSchema,
    DeviceCreateSchema,
    DeviceUpdateSchema,
    Error,
    DeviceLocationPatch,
)


app = NinjaAPI(version="1.0.0")


@app.get("/devices", response=list[DeviceSchema])
def get_devices(request):
    return Device.objects.all()


@app.post("/devices", response={200: DeviceSchema, 404: Error})
def create_device(request, device: DeviceCreateSchema):
    if device.location_id:
        # we have a location_id in the body
        location_exists = Location.objects.filter(id=device.location_id).exists()
        if not location_exists:
            return 404, {"message": "Location not found!"}

    device_data = device.model_dump()
    device_model = Device.objects.create(**device_data)
    return device_model


@app.get("/devices/{slug}", response=DeviceSchema)
def get_device_detail(request, slug: str):
    device = get_object_or_404(Device, slug=slug)
    return device


@app.put("/devices/{slug}", response=DeviceSchema)
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


@app.delete("/devices/{slug}")
def delete_device(request, slug: str):
    device = get_object_or_404(Device, slug=slug)
    device.delete()
    return {"deleted": True}


@app.post("/devices/{device_slug}/set-location", response=DeviceSchema)
def update_device_location(request, device_slug: str, location: DeviceLocationPatch):
    device = get_object_or_404(Device, slug=device_slug)
    if location.location_id:
        location = get_object_or_404(Location, id=location.location_id)
        device.location = location
    else:
        device.location = None

    device.save()
    return device


@app.get("/locations", response=list[LocationSchema])
def get_location(request):
    return Location.objects.all()
