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
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    @api.multi
    def write(self, vals):
        res = super(SaleOrder, self).write(vals)
        for each in self.order_line:
            if each.product_id and each.price_unit < each.product_id.standard_price:
                raise ValidationError(_('You can not sell the item for less than the Cost Price for %s.')%each.product_id.name)
        return res

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: