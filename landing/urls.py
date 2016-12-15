from django.conf.urls import url, include
from . import views
import subset.views as subset

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subset/', subset.index, name='index')
]
