from django.conf.urls import url, include
from . import views
import subset.views as subset
import datasets.views as datasets

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subset/', subset.index, name='index'),
    url(r'^datasets/', datasets.index, name='index')
]
