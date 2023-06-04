# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    amount_gross = fields.Float(string='GROSS', compute='_compute_fields', store=True)
    amount_net = fields.Float(string='NET', compute='_compute_fields', store=True)
    employee_image = fields.Binary(readonly=True, related='employee_id.image')

    @api.depends('line_ids')
    def _compute_fields(self):
        for record in self:

            gross, net = 0.0, 0.0
            for line in record.line_ids:
                if line.salary_rule_id.category_id.code == 'GROSS':
                    gross += line.total
                if line.salary_rule_id.category_id.code == 'NET':
                    net += line.total

            record.amount_gross = gross
            record.amount_net = net

    def update_line_ids(self):
        for record in self:
            gross_amount, net_amount, gross_total, net_total = 0.0, 0.0, 0.0, 0.0

            for line in record.line_ids:
                if line.salary_rule_id.category_id.code in ['BASIC', 'ALW']:
                    gross_amount += line.amount
                    gross_total += line.total
                if line.salary_rule_id.category_id.code in ['BASIC', 'ALW', 'DED']:
                    net_amount += line.amount
                    net_total += line.total

            # Apply
            for line in record.line_ids:
                if line.salary_rule_id.category_id.code == 'GROSS':
                    line.amount = gross_amount
                    line.total = gross_total

                if line.salary_rule_id.category_id.code == 'NET':
                    line.amount = net_amount
                    line.total = net_total

