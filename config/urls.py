from django.contrib import admin
from django.urls import path
from devices.api import app
from employee.api import api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", app.urls),
    path("api/v2/", api.urls),
]
