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

import fixtures
import os

from oslo.config import cfg

from cerberus.common import policy as cerberus_policy
from cerberus.openstack.common import policy as common_policy
from cerberus.tests import fake_policy

CONF = cfg.CONF


class PolicyFixture(fixtures.Fixture):

    def setUp(self):
        super(PolicyFixture, self).setUp()
        self.policy_dir = self.useFixture(fixtures.TempDir())
        self.policy_file_name = os.path.join(self.policy_dir.path,
                                             'policy.json')
        with open(self.policy_file_name, 'w') as policy_file:
            policy_file.write(fake_policy.policy_data)
        CONF.set_override('policy_file', self.policy_file_name)
        cerberus_policy._ENFORCER = None
        self.addCleanup(cerberus_policy.get_enforcer().clear)

    def set_rules(self, rules):
        common_policy.set_rules(common_policy.Rules(
            dict((k, common_policy.parse_rule(v))
                 for k, v in rules.items())))