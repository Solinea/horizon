from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.goldstone import dashboard

class Resources(horizon.Panel):
    name = _("Resources")
    slug = "resources"


dashboard.Goldstone.register(Resources)
