from .models import Dataset, MeasurementFile
import django_filters
from rest_framework_gis.filters import GeoFilterSet, GeometryFilter


class DatasetFilter(GeoFilterSet):
    """
    A filter for dataset API queries to allow querying the measurement type
    """
    measurement_type = django_filters.CharFilter(name='measurement__measurement_type')

    class Meta:
        model = Dataset
        fields = ['owner', 'public', 'measurement_type', 'campaign', 'platform_type']


class MeasurementFileFilter(GeoFilterSet):
    """
    A filter for measurement file API queries to allow querying intersection of a given geometry
    """
    intersects = GeometryFilter(name='spatial_extent', lookup_expr='intersects')
    dataset = django_filters.CharFilter(name='measurements__dataset')

    class Meta:
        model = MeasurementFile
        fields = ['filename', 'time_start', 'time_end']
