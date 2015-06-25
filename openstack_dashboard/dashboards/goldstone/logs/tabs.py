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
            self, token, marker=None,
            filter_field=None, filter_exp=None,
            resource_filter=None,
            url='http://127.0.0.1:8000/logging/search/'):

        headers = {'Authorization': 'Token ' + token}
        params = {}
        if filter_field is not None and filter_exp is not None:
            params[filter_field + '__regexp'] = '.*' \
                                                + filter_exp + \
                                                '.*'

        if resource_filter is not None:
            params['host'] = resource_filter

        if marker is not None:
            params['@timestamp__range'] = json.dumps({'lt': marker})

        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            result = json.loads(response.text)
            return result
        else:
            return None

    def has_more_data(self, table):
        return self._has_more

    def get_logs_data(self):
        try:
            resource_filter = None
            if hasattr(self.tab_group.kwargs, 'resource_id'):
                resource_filter = self.tab_group.kwargs['resource_id']
            marker = self.request.GET.get(
                tables.LogsTable._meta.pagination_param, None)
            filter_field = self.request.POST.get(
                'logs__filter__logs_filter_field', None)
            filter_exp = self.request.POST.get(
                'logs__filter__logs_filter', None)
            token = self.authenticate_goldstone()
            logs = self.get_goldstone_logs(token, marker,
                                           filter_field, filter_exp,
                                           resource_filter)
            self._has_more = logs['next'] is not None
            return logs['results']
        except Exception:
            self._has_more = False
            error_message = _('Unable to get logs')
            exceptions.handle(self.request, error_message)

            return []

class LogsTabs(tabs.TabGroup):
    slug = "logs_tabs"
    tabs = (LogsTab,)
    sticky = True
