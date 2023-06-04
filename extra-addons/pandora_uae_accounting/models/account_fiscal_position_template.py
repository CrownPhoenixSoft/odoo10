'''
Created on May 20 , 2019

@author: Faraz Zafar
'''
from odoo import models, api,fields

# Fiscal Position Templates as in code of odoo 10

class AccountFiscalPositionTemplate(models.Model):
    
    _inherit = 'account.fiscal.position.template'
    sequence = fields.Integer()
    auto_apply = fields.Boolean(string='Detect Automatically', help="Apply automatically this fiscal position.")
    vat_required = fields.Boolean(string='VAT required', help="Apply only if partner has a VAT number.")
    country_id = fields.Many2one('res.country', string='Country',
        help="Apply only if delivery or invoicing country match.")
    country_group_id = fields.Many2one('res.country.group', string='Country Group',
        help="Apply only if delivery or invoicing country match the group.")
    state_ids = fields.Many2many('res.country.state', string='Federal States')
    zip_from = fields.Integer(string='Zip Range From', default=0)
    zip_to = fields.Integer(string='Zip Range To', default=0)