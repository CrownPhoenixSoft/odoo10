# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import api, models, fields, _
import odoo.addons.decimal_precision as dp

class product_template(models.Model):
    _inherit = 'product.template'
        
    current_currency_id = fields.Many2one('res.currency', string="Current Currency")
    standard_price = fields.Float(
        'Cost of Current Company', compute='_compute_standard_price',
        inverse='_set_standard_price', search='_search_standard_price',
        digits=dp.get_precision('Product Price'), groups="base.group_user",
        help="Cost of the product, in the default unit of measure of the product.")
    

class res_users(models.Model):
    _inherit = 'res.users'
     
    @api.constrains('company_id')
    def check_current_company(self):
        for each in self.env['product.template'].search([]):
            each.current_currency_id = self.company_id.currency_id.id
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: