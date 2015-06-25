from django.utils.translation import ugettext_lazy as _

import horizon


class Goldstone(horizon.Dashboard):
    name = _("Goldstone")
    slug = "goldstone"
    panels = ('resources')  # Add your panels here.
    default_panel = 'resources'  # Specify the slug of the default panel.


horizon.register(Goldstone)
