from django.shortcuts import render, redirect
from datasets.models import MeasurementVariable, MeasurementFile
from .forms import DataSelection
from django.contrib import messages


def index(request, template_name='subset/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required

        files = MeasurementFile.objects.values_list('filename', flat=True).\
            filter(measurements__dataset=form.cleaned_data['dataset'],
                   time_end__gte=form.cleaned_data['start_date'],
                   time_start__lte=form.cleaned_data['end_date'],
                   measurements__measurement_type=form.cleaned_data['measurement']).all()

        if 'spatial_extent' in form.data:
            # Do this separately since it's optional, and probably slow
            files = files.filter(spatial_extent__intersects=form.data['spatial_extent'])

        if files:
            variables = MeasurementVariable.objects.values_list('variable_name', flat=True).\
                filter(measurement_type__measurement_type=form.cleaned_data['measurement'],
                       measurement_type__dataset=form.cleaned_data['dataset']).all()

            # redirect to a new URL:
            messages.add_message(request, messages.SUCCESS, 'cis subset {vars}:{files}'.format(vars=','.join(variables),
                                                                                            files=','.join(files)))
        else:
            messages.add_message(request, messages.ERROR, 'No matching files to subset')
        return redirect('/')
    else:
        files = None
        variables = None

        return render(request, template_name, {'form': form})
