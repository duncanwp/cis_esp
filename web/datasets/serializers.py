"""
Searilizers of all the model types for API usage
"""
from rest_framework import serializers
from .models import Campaign, Dataset, Measurement, MeasurementFile
from rest_framework_gis.serializers import GeoFeatureModelSerializer


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'


class DatasetSerializer(GeoFeatureModelSerializer):

    platform_type = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        # Set the spatial extent as a geo field for serialization
        geo_field = "spatial_extent"
        fields = ('id', 'name', 'platform_type', 'platform_name', 'region', 'public')

    def get_platform_type(self, obj):
        return obj.get_platform_type_display()


class MeasurementSerializer(serializers.ModelSerializer):

    measurement_type = serializers.SerializerMethodField()

    class Meta:
        model = Measurement
        fields = '__all__'

    def get_measurement_type(self, obj):
        return obj.get_measurement_type_display()


class MeasurementFileSerializer(GeoFeatureModelSerializer):

    class Meta:
        model = MeasurementFile
        # Set the spatial extent as a geo field for serialization
        geo_field = "spatial_extent"
        fields = ('id', 'filename', 'spatial_extent', 'time_start', 'time_end')
