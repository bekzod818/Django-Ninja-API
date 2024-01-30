import pytest
from .api import DeviceController, LocationController
from ninja_extra.testing import TestClient
from ninja_extra.testing import TestAsyncClient


# TestClient: for synchronous route functions
@pytest.mark.django_db
class TestDeviceController:
    def test_get_devices(self):
        client = TestClient(DeviceController)
        response = client.get('/devices')
        assert response.status_code == 200


# TestAsyncClient: for asynchronous route functions
class TesLocationController:
    def test_get_locations_async(self):
        client = TestAsyncClient(LocationController)
        response = client.get('/locations')
        assert response.status_code == 200
