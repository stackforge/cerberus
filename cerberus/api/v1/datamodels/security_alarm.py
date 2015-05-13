#
# Copyright (c) 2015 EUROGICIEL
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
#

import datetime

from cerberus.api.v1.datamodels import base
from wsme import types as wtypes


class SecurityAlarmResource(base.Base):
    """ Representation of a security alarm.
    """

    id = wtypes.IntegerType()
    """Security alarm id."""

    plugin_id = wtypes.wsattr(wtypes.text)
    """Associated plugin id."""

    alarm_id = wtypes.wsattr(wtypes.text)
    """Associated alarm id."""

    timestamp = datetime.datetime
    """creation date."""

    status = wtypes.wsattr(wtypes.text)
    """Status."""

    severity = wtypes.wsattr(wtypes.text)
    """Severity."""

    project_id = wtypes.wsattr(wtypes.text)
    """Associated project id."""

    component_id = wtypes.wsattr(wtypes.text)
    """Component id."""

    summary = wtypes.wsattr(wtypes.text)
    """Summary."""

    description = wtypes.wsattr(wtypes.text)
    """Description."""

    ticket_id = wtypes.wsattr(wtypes.text)
    """Associated ticket id."""

    def as_dict(self):
        return self.as_dict_from_keys(
            ['id', 'plugin_id', 'alarm_id', 'timestamp',
             'status', 'severity', 'component_id', 'project_id',
             'summary', 'description', 'ticket_id']
        )

    def __init__(self, initial_data=None):
        super(SecurityAlarmResource, self).__init__()
        if initial_data is not None:
            for key in initial_data:
                setattr(self, key, initial_data[key])

    @classmethod
    def sample(cls):
        sample = cls(initial_data={
            'id': 1,
            'plugin_id': '927c8435-f81f-468a-92cb-ebb08ed0fad2',
            'alarm_id': 'fea4b170-ed46-4a50-8b91-ed1c6876be7d',
            'timestamp': '2015-03-24 09:50:50.577840',
            'status': 'new',
            'severity': 'critical',
            'project_id': 'e845a1f2004847e4ac14cb1732a2e75f',
            'component_id': '4b75699f7a9649438932bebdbf9711e0',
            'summary': 'Several attempts to log failed',
            'description': 'Apache suffered an attack by brute force.'
                           ' Thousands of attempts to log failed'})
        return sample


class SecurityAlarmResourceCollection(base.Base):
    """A list of Security alarms."""

    security_alarms = [SecurityAlarmResource]
