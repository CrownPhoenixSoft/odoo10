from odoo import fields, api, models

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    display_name = fields.Char(compute='_compute_display_name', store=True, index=True)