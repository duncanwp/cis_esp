from django import forms
import datasets.models as model


class DataSelection(forms.Form):
    dummy = forms.CharField(label='Your name', max_length=100)
    # dataset = forms.Select(choices=model.Dataset)

