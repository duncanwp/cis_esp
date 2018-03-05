from django.conf.urls import url, include
from . import views
import subset.views as subset
import datasets.views as datasets
import collocate.views as collocate
import jobs.views as jobs
import visualise.views as visualise
import aggregate.views as aggregate
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
    url(r'^datasets/', datasets.index, name='index'),
    url(r'^visualise/', visualise.index, name='index'),
    url(r'^collocate/', collocate.index, name='index'),
    url(r'^aggregate/', aggregate.index, name='index'),
    url(r'^jobs/', jobs.index, name='index'),
    url(r'^api/', include(router.urls)),
]
