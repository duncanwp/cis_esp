from django.contrib.gis import forms
import datasets.models as model
from datetime import datetime


class DataSelection(forms.Form):

    measurement = forms.ChoiceField(choices=[("", "---------")] + list(model.Measurement.MEASUREMENT_TYPE_CHOICES))
    dataset = forms.ModelChoiceField(queryset=model.Dataset.objects.all())

    # TODO For some reason django can't resolve this relationship...
    # start_date = forms.DateField(widget=forms.SelectDateWidget(years=[d.year for d in model.MeasurementFile.objects.all().datetimes('time_start', 'year')]))
    start_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1960, 2017)))
    end_date = forms.DateField(widget=forms.SelectDateWidget(years=range(1960, 2017)), initial=datetime(2016,12,31))

    # The spatial extent gets added by the JS

    subset_dataset = forms.ModelChoiceField(queryset=model.Dataset.objects.all())
