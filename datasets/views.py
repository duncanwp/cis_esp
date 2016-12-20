from django.shortcuts import render, redirect
from django.core.serializers import serialize
from datasets.models import Dataset, Campaign, MeasurementVariable, MeasurementFile
from .forms import DataSelection


def index(request, template_name='datasets/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # return redirect('#')

        geoms = MeasurementFile.objects.filter(time_end__gte=form.cleaned_data['start_date'],
                                               time_start__lte=form.cleaned_data['end_date'],
                                               measurements__measurement_type=form.cleaned_data['measurement'],
                                               measurements__dataset__in=form.cleaned_data['datasets']).all()

        # if len(geoms) > 10:
        #     print('Warning')
        #     geoms = geoms[:10]
        feature = serialize('geojson', geoms,
                            geometry_field='spatial_extent')
    else:
        feature = None

    return render(request, template_name, {'form': form, 'geojsonFeature': feature})
