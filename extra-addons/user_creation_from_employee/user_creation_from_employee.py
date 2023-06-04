# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: Nilmar Shereef(<http://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api, _


class ResUsersInherit(models.Model):
    _inherit = 'hr.employee'

    user_check_tick = fields.Boolean(default=False)

    @api.multi
    def create_user(self):
        user_id = self.env['res.users'].create({'name': self.name,'login': self.work_email})
        self.address_home_id = user_id.partner_id.id
        self.user_check_tick = True
        self.user_id=user_id.id

        user_id.partner_id.email=self.work_email
        user_id.partner_id.image=self.image

        if self.company_id.account_employee_receivable:

            user_id.partner_id.property_account_receivable_id=self.company_id.account_employee_receivable


        if self.company_id.account_employee_payable:

            user_id.partner_id.property_account_payable_id=self.company_id.account_employee_payable



    @api.onchange('address_home_id')
    def user_checking(self):
        if self.address_home_id:
            self.user_check_tick = True
        else:
            self.user_check_tick = False



class CompanyUser(models.Model):

    _inherit = 'res.company'

    account_employee_receivable=fields.Many2one('account.account',string="Employee Receivable Account")
    account_employee_payable =fields.Many2one('account.account',string="Employee Payable Account")

