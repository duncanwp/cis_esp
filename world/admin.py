from django.contrib.gis import admin
from .models import WorldBorder

# Use the default admin page with a Vector Map Level 0 WMS dataset background
# admin.site.register(WorldBorder, admin.GeoModelAdmin)

# Use the Open-Street map admin page
admin.site.register(WorldBorder, admin.OSMGeoAdmin)
