from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import forms

from openstack_dashboard import api


class CreateSnapshot(forms.SelfHandlingForm):
    instance_id = forms.CharField(label=_("Instance ID"),
                                  widget=forms.HiddenInput(),
                                  required=False)
    name = forms.CharField(max_length=255, label=_("Snapshot Name"))

    def handle(self, request, data):
        try:
            snapshot = api.nova.snapshot_create(request,
                                                data['instance_id'],
                                                data['name'])
            return snapshot
        except Exception:
            exceptions.handle(request,
                              _('Unable to create snapshot.'))
