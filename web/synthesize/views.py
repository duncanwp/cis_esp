from django.shortcuts import render, redirect
from datasets.models import MeasurementVariable, MeasurementFile, Region
from .forms import DataSelection
from django.contrib import messages


def index(request, template_name='synthesize/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required

        files = MeasurementFile.objects.values_list('name', flat=True).\
            filter(measurements__measurement_type=form.cleaned_data['measurement']).all()

        spatial_extent = None

        if form.cleaned_data['subset_region']:
            spatial_extent = Region.objects.filter(id=form.data['subset_region']).first().spatial_extent
        elif 'spatial_extent' in form.data:
            spatial_extent = form.data['spatial_extent']
        else:
            messages.add_message(request, messages.ERROR, 'No spatial extent specified')

        files = files.filter(spatial_extent__intersects=spatial_extent)

        if files:
            variables = MeasurementVariable.objects.values_list('variable_name', flat=True).\
                filter(measurement_type__measurement_type=form.cleaned_data['measurement']).all()

            # redirect to a new URL:
            messages.add_message(request, messages.SUCCESS, 'cis aggregate {vars}:{files}'.format(vars=','.join(variables), files=','.join(files)))
            # TODO - create a CIS_Job
        else:
            messages.add_message(request, messages.ERROR, 'No matching files to subset')

        return redirect('/jobs')
    else:
        files = None
        variables = None

        return render(request, template_name, {'form': form})
