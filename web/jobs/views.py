from django.shortcuts import render
import arc


def index(request):
    return render(request, 'jobs/index.html')
