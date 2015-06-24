from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.mydashboard.mypanel import views


urlpatterns = patterns('',
    url(r'^$',
        views.IndexView.as_view(), name='index'),
    url(r'^(?P<instance_id>[^/]+)/create_snapshot/$',
    views.CreateSnapshotView.as_view(),
    name='create_snapshot'),
)
