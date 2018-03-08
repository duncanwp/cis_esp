from django.contrib.gis import forms
import datasets.models as model


class DataSelection(forms.Form):

    measurement = forms.ChoiceField(choices=[("", "---------")] + list(model.Measurement.MEASUREMENT_TYPE_CHOICES))

    subset_region = forms.ModelChoiceField(queryset=model.Region.objects.all(), required=False)
