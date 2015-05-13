#
#   Copyright (c) 2015 EUROGICIEL
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

import pecan
from webob import exc
from wsme import types as wtypes
import wsmeext.pecan as wsme_pecan

from cerberus.api.v1.controllers import base
from cerberus.api.v1.datamodels import security_report as report_models
from cerberus.common import errors
from cerberus import db
from cerberus.db.sqlalchemy import models
from cerberus.openstack.common import log

LOG = log.getLogger(__name__)


class SecurityReportsController(base.BaseController):

    @pecan.expose()
    def _lookup(self, report_id, *remainder):
        return SecurityReportController(report_id), remainder

    def list_security_reports(self, project_id=None):
        """ List all the security reports of all projects or just one. """
        try:
            security_reports = db.security_report_get_all(
                project_id=project_id)
        except Exception as e:
            LOG.exception(e)
            raise errors.DbError(
                "Security reports could not be retrieved"
            )
        return security_reports

    @wsme_pecan.wsexpose(report_models.SecurityAlarmResourceCollection)
    def get_all(self):
        """ Get stored security reports.
        :return: list of security reports for one or all projects depending on
        context of the token.
        """
        ctx = pecan.request.context
        try:
            if ctx.is_admin:
                security_reports = self.list_security_reports()
            else:
                security_reports = self.list_security_reports(ctx.tenant_id)
        except errors.DbError:
            raise exc.HTTPNotFound()

        reports_resource = []
        # todo(eglamn3) : no need to serialize here
        for security_report in security_reports:
            reports_resource.append(
                report_models.SecurityAlarmResource(
                    models.SecurityReportJsonSerializer().
                    serialize(security_report)))

        return report_models.SecurityAlarmResourceCollection(
            security_reports=reports_resource)


class SecurityReportController(base.BaseController):

    _custom_actions = {
        'tickets': ['PUT']
    }

    def __init__(self, report_id):
        super(SecurityReportController, self).__init__()
        pecan.request.context['report_id'] = report_id
        try:
            self._id = int(report_id)
        except ValueError:
            raise exc.HTTPBadRequest(
                explanation='Security report id must be an integer')

    def get_security_report(self, id):
        try:
            security_report = db.security_report_get(id)
        except Exception as e:
            LOG.exception(e)
            raise errors.DbError(
                "Security report %s could not be retrieved" % id
            )
        return security_report

    @wsme_pecan.wsexpose(report_models.SecurityAlarmResource,
                         wtypes.text)
    def get(self):
        """Get security report in db. """
        try:
            security_report = self.get_security_report(self._id)
        except errors.DbError:
            raise exc.HTTPNotFound()
        s_report = models.SecurityReportJsonSerializer().\
            serialize(security_report)

        return report_models.SecurityAlarmResource(initial_data=s_report)

    @pecan.expose("json")
    def tickets(self, ticket_id):
        """Modify the ticket id associated to a security report in db.

        :param ticket_id: the ticket_id to store in db.

        """
        try:
            db.security_report_update_ticket_id(self._id, ticket_id)
        except Exception:
            raise exc.HTTPNotFound()