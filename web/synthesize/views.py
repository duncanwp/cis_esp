from django.shortcuts import render, redirect
from datasets.models import Dataset, MeasurementVariable, MeasurementFile
from .forms import DataSelection
from django.contrib import messages


def index(request, template_name='synthesize/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required

        files = MeasurementFile.objects.values_list('name', flat=True).\
            filter(measurements__dataset=form.cleaned_data['dataset'],
                   measurements__measurement_type=form.cleaned_data['measurement']).all()

        spatial_extent = None

        if form.cleaned_data['subset_dataset']:
            subset_dataset = Dataset.objects.filter(id=form.data['subset_dataset']).first()

            spatial_extent = subset_dataset.spatial_extent
            start_date = subset_dataset.time_start
            end_date = subset_dataset.time_end
        else:
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            if 'spatial_extent' in form.data:
                spatial_extent = form.data['spatial_extent']
            elif form.cleaned_data['subset_region']:
                spatial_extent = None  #TODO

        files = files.filter(time_end__gte=start_date, time_start__lte=end_date)

        if spatial_extent:
            files = files.filter(spatial_extent__intersects=spatial_extent)

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
