from rest_framework import serializers
from .models import Dataset, Measurement


class DatasetSerializer(serializers.ModelSerializer):

    platform_type = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'platform_type', 'platform_name', 'region', 'public')

    def get_platform_type(self, obj):
        return obj.get_platform_type_display()
