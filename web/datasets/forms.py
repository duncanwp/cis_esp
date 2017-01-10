from django.contrib.gis import forms
import datasets.models as model


class DataSelection(forms.Form):

    measurement = forms.ChoiceField(choices=[("", "---------")] + list(model.Measurement.MEASUREMENT_TYPE_CHOICES))
    datasets = forms.ModelMultipleChoiceField(queryset=model.Dataset.objects.all(), required=False)
    measurement_files = forms.ModelMultipleChoiceField(queryset=model.MeasurementFile.objects.all(), required=False)
