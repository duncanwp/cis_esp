from django.conf.urls import url, include
from . import views
import subset.views as subset
import datasets.views as datasets
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'campaign', datasets.CampaignViewSet)
router.register(r'datasets', datasets.DatasetViewSet)
router.register(r'measurements', datasets.MeasurementViewSet)
router.register(r'measurement-files', datasets.MeasurementFileViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^subset/', subset.index, name='index'),
    url(r'^datasets/parent-to-children/$', datasets.parent_to_children),
    url(r'^datasets/', datasets.index, name='index'),
    url(r'^api/', include(router.urls, namespace='api')),
]
