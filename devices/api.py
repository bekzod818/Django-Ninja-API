from django.shortcuts import get_object_or_404
from ninja import NinjaAPI
from .models import Location, Device
from .schemas import LocationSchema, DeviceSchema


app = NinjaAPI()


@app.get("/devices", response=list[DeviceSchema])
def get_devices(request):
    return Device.objects.all()


@app.get("/devices/{slug}", response=DeviceSchema)
def get_device_detail(request, slug: str):
    device = get_object_or_404(Device, slug=slug)
    return device


@app.get("/locations", response=list[LocationSchema])
def get_location(request):
    return Location.objects.all()
