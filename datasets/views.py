from django.shortcuts import render, redirect, HttpResponse
from django.core.serializers import serialize
from rest_framework import viewsets, filters
from .models import Dataset, Campaign, Measurement, MeasurementFile
from .forms import DataSelection
from .serializers import DatasetSerializer, MeasurementSerializer, MeasurementFileSerializer, CampaignSerializer
from .filters import DatasetFilter


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
    filter_backends = (filters.DjangoFilterBackend,)
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
    queryset = MeasurementFile.objects.all()
    serializer_class = MeasurementFileSerializer


def index(request, template_name='datasets/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # return redirect('#')

        geoms = MeasurementFile.objects.filter(time_end__gte=form.cleaned_data['start_date'],
                                               time_start__lte=form.cleaned_data['end_date'],
                                               measurements__measurement_type=form.cleaned_data['measurement']).all()

        # Include all datasets if none are chosen
        if form.cleaned_data['datasets']:
            geoms = geoms.filter(measurements__dataset__in=form.cleaned_data['datasets'])

        # Don't set a max limit - I might have to revisit this depending on performance
        # if len(geoms) > 10:
        #     print('Warning')
        #     geoms = geoms[:10]
        feature = serialize('geojson', geoms,
                            geometry_field='spatial_extent')
    else:
        feature = None

    return render(request, template_name, {'form': form, 'geojsonFeature': feature})


def parent_to_children(request):
    import json

    parent=request.GET.get('measurement')
    ret=[]
    if parent:
        for child in Dataset.objects.filter(measurement__measurement_type=parent):
            ret.append(dict(id=child.id, value=child))
    if len(ret)!=1:
        ret.insert(0, dict(id='', value='---'))
    return HttpResponse(json.dumps(ret), content_type='application/json')
