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

from openstack_dashboard.dashboards.goldstone.logs import tables

import requests
import json

import logging
LOG = logging.getLogger(__name__)


class LogsTab(tabs.TableTab):
    name = _("Logs Tab")
    slug = "logs_tab"
    table_classes = (tables.LogsTable,)
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

    def get_goldstone_logs(
            self, token,
            query_filter=None,
            url='http://127.0.0.1:8000/logging/search/'):

        headers = {'Authorization': 'Token ' + token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result
        else:
            return None

    def get_logs_data(self):
        try:
            token = self.authenticate_goldstone()
            logs = self.get_goldstone_logs(token)
            return logs['results']
        except Exception:
            error_message = _('Unable to get logs')
            exceptions.handle(self.request, error_message)

            return []

class LogsTabs(tabs.TabGroup):
    slug = "logs_tabs"
    tabs = (LogsTab,)
    sticky = True
