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
from horizon import tables
from horizon.templatetags import sizeformat
from django.utils.translation import ugettext_lazy as _

class MyFilterAction(tables.FilterAction):
    name = "myfilter"

class LogsTable(tables.DataTable):
    hostname = tables.Column("@timestamp",
                             attrs={'data-type': 'naturalSort'},
                             verbose_name=_("Timestamp"))

    severity = tables.Column("syslog_severity",
                             verbose_name=_("Syslog Severity"))

    component = tables.Column("component",
                              verbose_name=_("Component"))

    host = tables.Column("host",
                         verbose_name=_("Host"))

    message = tables.Column('log_message',
                            verbose_name=_("Message"))

    def get_object_id(self, log_entry):
        return "%s" % (log_entry['@timestamp'])

    class Meta(object):
        name = "logs"
        verbose_name = _("Logs")
        table_actions = (MyFilterAction,)

