# Register your models here.
from django.contrib.gis import admin
from .models import *

# Use the default admin page with a Vector Map Level 0 WMS dataset background
# default_admin = admin.GeoModelAdmin

default_admin = admin.OSMGeoAdmin

# Use the Open-Street map admin page
admin.site.register(Measurement, admin.ModelAdmin)
admin.site.register(MeasurementVariable, admin.ModelAdmin)
admin.site.register(MeasurementFile, default_admin)
admin.site.register(Region, default_admin)
admin.site.register(CIS_Job, admin.ModelAdmin)
admin.site.register(AggregationResult, default_admin)
