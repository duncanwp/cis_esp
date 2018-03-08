from .models import MeasurementFile
import django_filters
from rest_framework_gis.filters import GeoFilterSet, GeometryFilter


class MeasurementFileFilter(GeoFilterSet):
    """
    A filter for measurement file API queries to allow querying intersection of a given geometry
    """
    intersects = GeometryFilter(name='spatial_extent', lookup_expr='intersects')
    dataset = django_filters.CharFilter(name='measurements__dataset')

    class Meta:
        model = MeasurementFile
        fields = ['name', 'time_start', 'time_end']
