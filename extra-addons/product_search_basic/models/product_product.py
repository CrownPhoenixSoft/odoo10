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

from odoo import api, models, _

class product_product(models.Model):
    _inherit = 'product.product'
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        return super(product_product, self).name_search(name= name.replace(' ','%'), args=None, operator='ilike', limit=100)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: