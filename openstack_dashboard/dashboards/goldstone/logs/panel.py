from django.utils.translation import ugettext_lazy as _

import horizon
from openstack_dashboard.dashboards.goldstone import dashboard

class Logs(horizon.Panel):
    name = _("Logs")
    slug = "logs"
    permissions = ('openstack.roles.admin',)


dashboard.Goldstone.register(Logs)
