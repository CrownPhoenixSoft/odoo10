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

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    tax_amount = fields.Float(string="Tax Amount", compute='_compute_amount_tax')

    @api.depends('quantity', 'discount', 'price_unit', 'invoice_line_tax_ids')
    def _compute_amount_tax(self):
        for line in self:
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = line.invoice_line_tax_ids.compute_all(price, line.invoice_id.currency_id, line.quantity,
                                            product=line.product_id, partner=line.invoice_id.partner_id)
            line.update({
                'tax_amount': taxes['total_included'] - taxes['total_excluded']
            })
            
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: