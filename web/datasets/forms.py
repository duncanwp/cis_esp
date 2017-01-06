from django.contrib.gis import forms
import datasets.models as model
from datetime import datetime


class DataSelection(forms.Form):

    measurement = forms.ChoiceField(choices=[("", "---------")] + list(model.Measurement.MEASUREMENT_TYPE_CHOICES))
    datasets = forms.ModelMultipleChoiceField(queryset=model.Dataset.objects.all(), required=False)
