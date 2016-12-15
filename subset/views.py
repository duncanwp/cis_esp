from django.shortcuts import render, redirect

from .forms import DataSelection


def index(request, template_name='subset/index.html'):

    form = DataSelection(request.POST or None)

    if form.is_valid():
        # process the data in form.cleaned_data as required
        # ...
        # redirect to a new URL:
        return redirect('#')

    return render(request, template_name, {'form': form})
