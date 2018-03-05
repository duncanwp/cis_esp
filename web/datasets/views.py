from django.shortcuts import render
from rest_framework import viewsets, filters
from .models import Dataset, Campaign, Measurement, MeasurementFile
from .forms import DataSelection
from .serializers import DatasetSerializer, MeasurementSerializer, MeasurementFileSerializer, CampaignSerializer
from .filters import DatasetFilter, MeasurementFileFilter


class CampaignViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer


class DatasetViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    filter_class = DatasetFilter

    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer


class MeasurementViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer


class MeasurementFileViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    filter_class = MeasurementFileFilter

    queryset = MeasurementFile.objects.all()
    serializer_class = MeasurementFileSerializer


def index(request):
    """
    Render the browser
    """

    return render(request, 'datasets/index.html', {'form': DataSelection()})
