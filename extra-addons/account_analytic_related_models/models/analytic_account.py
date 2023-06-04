# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from unicodedata import normalize
from urllib import urlencode
from odoo import fields, models, api

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account',ondelete="cascade", auto_join=True)

    @api.model
    def create(self, vals):
        res = super(HrEmployee, self).create(vals)
        if not vals.get('analytic_account_id'):
            analytic_id = self.env['account.analytic.account'].create({'name': vals.get('name').encode('utf-8'),
                                                                       'analytic_account_type': 'Employee'})
            res['analytic_account_id'] = analytic_id
        return res

    def related_costs(self):
        action = {
            'name': 'Analytic Account Line',
            'res_model': 'account.analytic.line',
            'view_mode': 'tree,form',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'context':{'search_default_group_date':1}
        }
        return action

class FleetVehicle(models.Model):
    _inherit = "fleet.vehicle"

    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account',ondelete="cascade", auto_join=True)

    @api.model
    def create(self, vals):
        res = super(FleetVehicle, self).create(vals)
        if not vals.get('analytic_account_id'):
            analytic_id = self.env['account.analytic.account'].create({'name': vals.get('license_plate').encode('utf-8'),
                                                                       'analytic_account_type': 'Fleet'})
            res['analytic_account_id'] = analytic_id
            analytic_id.vehicle_id = res.id
        return res
    
    def related_costs(self):
        action = {
            'name': 'Analytic Account Line',
            'res_model': 'account.analytic.line',
            'view_mode': 'tree,form',
            'target': 'current',
            'type': 'ir.actions.act_window',
            'domain': [('account_id', '=', self.analytic_account_id.id)],
            'context':{'search_default_group_date':1}
        }
        return action
    
    
class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"


    analytic_account_type = fields.Selection([('Project', 'Project'),('Employee', 'Employee'),('Fleet','Fleet')], string='Analytic Account Type', default='Project')
    vehicle_id = fields.Many2one('fleet.vehicle',string='Fleet Vehicle')

    @api.model
    def create(self, vals):
        analytic_account = super(AccountAnalyticAccount, self).create(vals)
        analytic_account['analytic_account_type'] = 'Project'
        return analytic_account

class FleetVehicleCost(models.Model):
    _inherit = "fleet.vehicle.cost"

    analytic_account_line_id = fields.Many2one(
        'account.analytic.line', string='Analytic Account Line')


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: