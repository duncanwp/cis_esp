from rest_framework import serializers
from .models import Campaign, Dataset, Measurement, MeasurementFile


class CampaignSerializer(serializers.ModelSerializer):

    class Meta:
        model = Campaign
        fields = '__all__'


class DatasetSerializer(serializers.ModelSerializer):

    platform_type = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = '__all__'

    def get_platform_type(self, obj):
        return obj.get_platform_type_display()


class MeasurementSerializer(serializers.ModelSerializer):

    measurement_type = serializers.SerializerMethodField()

    class Meta:
        model = Measurement
        fields = '__all__'

    def get_measurement_type(self, obj):
        return obj.get_measurement_type_display()


class MeasurementFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = MeasurementFile
        fields = '__all__'
