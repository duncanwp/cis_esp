from django.shortcuts import render
from rest_framework import viewsets
from .models import Measurement, MeasurementFile, Region, AggregationResult
from .forms import DataSelection
from .serializers import MeasurementSerializer, MeasurementFileSerializer, RegionSerializer, AggregationResultSerializer
from .filters import MeasurementFileFilter


class AggregationResultViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = AggregationResult.objects.all()
    serializer_class = AggregationResultSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


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
