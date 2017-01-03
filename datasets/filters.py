from .models import Dataset
import django_filters
from rest_framework_gis.filters import GeoFilterSet


class DatasetFilter(GeoFilterSet):
    """
    A filter for dataset API queries to allow querying the measurement type
    """
    measurement_type = django_filters.CharFilter(name='measurement__measurement_type')

    class Meta:
        model = Dataset
        fields = ['owner', 'public', 'measurement_type', 'campaign', 'platform_type']
