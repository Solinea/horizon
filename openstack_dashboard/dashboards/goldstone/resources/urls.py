from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.goldstone.resources import views


urlpatterns = patterns(
    '', url(r'^$', views.IndexView.as_view(), name='index'),
)
