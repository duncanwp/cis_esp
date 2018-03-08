"""
Searilizers of all the model types for API usage
"""
from rest_framework import serializers
from .models import Measurement, MeasurementFile, Region
import json


class RegionSerializer(serializers.ModelSerializer):

    spatial_extent = serializers.SerializerMethodField()

    class Meta:
        model = Region
        fields = '__all__'

    def get_spatial_extent(self, obj):
        # Get the GeoJSON for this field directly - rest_framework_gis doesn't seem to do GeometryCollections properly
        # Cast the resulting json to a json object so that the serializer doesn't escape it
        return json.loads(obj.spatial_extent.json) if obj.spatial_extent is not None else None


class MeasurementSerializer(serializers.ModelSerializer):

    measurement_type = serializers.SerializerMethodField()

    class Meta:
        model = Measurement
        fields = '__all__'

    def get_measurement_type(self, obj):
        return obj.get_measurement_type_display()


class MeasurementFileSerializer(serializers.ModelSerializer):

    spatial_extent = serializers.SerializerMethodField()

    class Meta:
        model = MeasurementFile
        fields = '__all__'

    def get_spatial_extent(self, obj):
        # Get the GeoJSON for this field directly
        # Cast the resulting json to a json object so that the serializer doesn't escape it
        return json.loads(obj.spatial_extent.json) if obj.spatial_extent is not None else None
