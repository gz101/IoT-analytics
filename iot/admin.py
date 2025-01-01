from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    DeviceType,
    Device,
    SensorData,   
)


admin.site.register(DeviceType)
admin.site.register(Device)
admin.site.register(SensorData)
