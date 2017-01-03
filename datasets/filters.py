# from django_filters.rest_framework import FilterSet, ModelChoiceFilter
# from rest_framework import filters
from .models import Dataset
import django_filters
from rest_framework_gis.filters import GeoFilterSet


class DatasetFilter(GeoFilterSet):
    measurement_type = django_filters.ModelChoiceFilter(name='measurement__measurement_type')

    class Meta:
        model = Dataset
        fields = ['owner', 'public', 'measurement_type', 'campaign', 'platform_type']
