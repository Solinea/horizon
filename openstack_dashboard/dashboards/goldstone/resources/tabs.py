# Copyright 2015 Solinea, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either expressed or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.utils.translation import ugettext_lazy as _

from horizon import exceptions
from horizon import tabs

from openstack_dashboard import api
from openstack_dashboard.dashboards.goldstone.resources import tables

import requests
import json

import logging
LOG = logging.getLogger(__name__)


class ResourcesTab(tabs.TableTab):
    name = _("Resources Tab")
    slug = "resources_tab"
    table_classes = (tables.ResourceTable,)
    template_name = ("horizon/common/_detail_table.html")
    preload = False

    @staticmethod
    def authenticate_goldstone(url='http://127.0.0.1:8000/accounts/login/',
                               user='admin', password='goldstone'):
        response = requests.post(url,
                                 data={'username': user, 'password': password})

        if response.status_code == 200:
            return json.loads(response.text)['auth_token']
        else:
            return None

    def get_goldstone_hypervisors(
            self, token, url='http://127.0.0.1:8000/nova/hypervisors/'):

        headers = {'Authorization': 'Token ' + token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result
        else:
            return None

    def get_resources_data(self):
        try:
            token = self.authenticate_goldstone()
            hypervisors = self.get_goldstone_hypervisors(token)
            return hypervisors[0]
        except Exception:
            error_message = _('Unable to get hypervisors')
            exceptions.handle(self.request, error_message)

            return []

class ResourcesTabs(tabs.TabGroup):
    slug = "resources_tabs"
    tabs = (ResourcesTab,)
    sticky = False
