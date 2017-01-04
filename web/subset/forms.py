from django.contrib.gis import forms
import datasets.models as model


class DataSelection(forms.Form):
    # Select the dataset
    dataset = forms.ModelChoiceField(queryset=model.Dataset.objects.all())

    # All of these need to be updated based on the above...
    variables = forms.ModelMultipleChoiceField(queryset=model.MeasurementVariable.objects.all())

    # TODO For some reason django can't resolve this relationship...
    # start_date = forms.DateField(widget=forms.SelectDateWidget(years=[d.year for d in model.MeasurementFile.objects.all().datetimes('time_start', 'year')]))
    start_date = forms.DateField(widget=forms.SelectDateWidget())
    end_date = forms.DateField(widget=forms.SelectDateWidget())

    # I'd like to restrict this to a rectangle somehow... and probably have the option for text entry
    # region = forms.PolygonField(widget=forms.OSMWidget(attrs={'map_width': 800, 'map_height': 500}))