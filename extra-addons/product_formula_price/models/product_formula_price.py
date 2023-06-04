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

from odoo import models, api, fields, _
    
class Pricelist(models.Model):
    _inherit = "product.pricelist.item"

    amount_pricelist = fields.Float(string= 'TOTAL', compute="_get_calc_display_price")

    def _get_calc_display_price(self):
        for each in self:
            prices = {}
            if each.pricelist_id and each.pricelist_id.id:
                pricelist = each.pricelist_id
                partner = self._context.get('partner', False)
                quantity = self._context.get('quantity', 1.0)
                if self.env.context.get('default_product_tmpl_id'):
                    prod_id = self.env['product.template'].browse(self.env.context.get('default_product_tmpl_id'))
                else:
                    if each.applied_on == '1_product':
                        prod_id = each.product_tmpl_id
                    elif each.applied_on == '0_product_variant':
                        prod_id = each.product_id.product_tmpl_id
                if prod_id and prod_id.id:
                    quantities = [quantity] * len(each)
                    partners = [partner] * len(each)
                    prices = pricelist.get_products_price(prod_id, quantities, partners)
            each.amount_pricelist = prices.get(prod_id.id, 0.0)