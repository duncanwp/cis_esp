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

        if form.cleaned_data['subset_region']:
            region = Region.objects.filter(id=form.data['subset_region']).first()
            spatial_extent = region.spatial_extent
            cis_extent = region.cis_extent
        elif 'spatial_extent' in form.data:
            spatial_extent = form.data['spatial_extent']
            # TODO turn the user defined extent into a CIS one
            cis_extent = ""
        else:
            messages.add_message(request, messages.ERROR, 'No spatial extent specified')
            return redirect('/jobs')

        files = files.filter(spatial_extent__intersects=spatial_extent)

        if files:
            variables = MeasurementVariable.objects.values_list('variable_name', flat=True).\
                filter(measurement_type__measurement_type=form.cleaned_data['measurement']).all()

            # redirect to a new URL:
            messages.add_message(request, messages.SUCCESS, 'cis aggregate {extent} {vars}:{files}'.format(extent=cis_extent, vars=','.join(variables), files=','.join(files)))
            # TODO - create a CIS_Job
        else:
            messages.add_message(request, messages.ERROR, 'No matching files')

        return redirect('/jobs')
    else:
        return render(request, template_name, {'form': form})
