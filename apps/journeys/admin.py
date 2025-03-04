from django.contrib import admin

from .models import (
    Country,
    City,
    Flight,
    FlightEvent
)

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Flight)
admin.site.register(FlightEvent)
