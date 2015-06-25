from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.goldstone.logs.views \
    import IndexView


urlpatterns = patterns(
    '',
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^(?P<resource_id>[^/]+)$', IndexView.as_view(), name='filtered_index'),
)
