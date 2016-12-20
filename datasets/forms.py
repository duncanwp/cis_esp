from django.contrib.gis import forms
import datasets.models as model
from datetime import datetime

class DataSelection(forms.Form):
    # Select the measurement
    measurement = forms.ChoiceField(choices=[("", "---------")] + list(model.Measurement.MEASUREMENT_TYPE_CHOICES))

    # All of these need to be updated based on the above...

    datasets = forms.ModelMultipleChoiceField(queryset=model.Dataset.objects.all(), required=False)

    all_years = [d.year for d in model.MeasurementFile.objects.all().datetimes('time_start', 'year')]
    if all_years:
        valid_years = range(min(all_years), max(all_years))
    else:
        valid_years = range(1990, 2010)

    start_date = forms.DateField(widget=forms.SelectDateWidget(years=valid_years))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=valid_years), initial=datetime(valid_years[-1], 1, 1))
