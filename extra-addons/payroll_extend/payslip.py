# -*- coding: utf-8 -*-
from openerp import fields, models, api, _

class hr_payslip(models.Model):
    _name = 'hr.payslip'
    _inherit = ['hr.payslip', 'mail.thread']
    
    _order = 'id desc'
    
    state = fields.Selection(track_visibility='onchange')
    
    
class hr_payslip_run(models.Model):
    _name = 'hr.payslip.run'
    _inherit = ['hr.payslip.run', 'mail.thread']
    
    _order = 'id desc'
    
    state = fields.Selection(track_visibility='onchange')

