from django.shortcuts import render, redirect
from django.core.serializers import serialize
from datasets.models import Dataset, Campaign, MeasurementVariable, MeasurementFile
from .forms import DataSelection


def index(request, template_name='subset/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        # return redirect('#')
        feature = serialize('geojson', MeasurementFile.objects.filter(time_end__gte=form.cleaned_data['start_date'],
                                                                      time_start__lte=form.cleaned_data['end_date'],
                                                                      measurements__measurementvariable__in=form.cleaned_data['variables']),
                            geometry_field='spatial_extent')
    else:
        feature = None

    return render(request, template_name, {'form': form, 'geojsonFeature': feature})
