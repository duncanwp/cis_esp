from django.conf.urls import url, include
from . import views
import datasets.views as datasets
import jobs.views as jobs
import synthesize.views as synthesize
import about.views as about
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'regions', datasets.RegionViewSet)
router.register(r'results', datasets.AggregationResultViewSet)
router.register(r'measurements', datasets.MeasurementViewSet)
router.register(r'measurement-files', datasets.MeasurementFileViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^datasets/', datasets.index, name='index'),
    url(r'^synthesize/', synthesize.index, name='index'),
    url(r'^jobs/', jobs.index, name='index'),
    url(r'^about/', about.index, name='index'),
    url(r'^api/', include(router.urls)),
]
