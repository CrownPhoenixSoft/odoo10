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

from odoo import api, fields, models


class sale_margin(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_confirm(self):
        discnt = 0.0
        no_line = 0.0
        for order in self:
            order.check_limit()
            if order.company_id.discount_approval:
                for line in order.order_line:
                    no_line += 1
                    discnt += line.discount
                discnt = (discnt / no_line)
                if order.company_id.limit_discount and discnt > order.company_id.limit_discount:
                    order.state = 'waiting'
                    return True
            if order.company_id.less_margin_approval:
                for line in order.order_line:
                    if line.price_unit == 0.00:
                        margin_percentage = 0.00
                    else:
                        margin_percentage = (line.margin * 100) / line.price_unit
                    print '\n\nmargin_percentage', margin_percentage
                    if order.company_id.at_least_margin and order.company_id.at_least_margin > margin_percentage:
                        order.state = 'waiting' 
                        return True
            order.state = 'sale'
            order.confirmation_date = fields.Datetime.now()
            if self.env.context.get('send_email'):
                self.force_quotation_send()
            order.order_line._action_procurement_create()
        if self.env['ir.values'].get_default('sale.config.settings', 'auto_done_setting'):
            self.action_done()
        return True


class Company(models.Model):
    _inherit = 'res.company'

    at_least_margin = fields.Float(string="Margin less than limit requires approval %",
                                    help="At lease margin after which approval of sale is required.")
    less_margin_approval = fields.Boolean(string="Force two levels of approvals for less margin.",
                                    help="Provide a double validation mechanism for sale margin inferior than At Least Margin.")

    @api.multi
    def set_default_discount(self):
        if self.less_margin_approval and self.less_margin_approval != self.company_id.less_margin_approval:
            self.company_id.write({'less_margin_approval': self.less_margin_approval})
        if self.at_least_margin and self.at_least_margin != self.company_id.at_least_margin:
            self.company_id.write({'at_least_margin': at_least_margin})


class AccountDiscountSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    at_least_margin = fields.Float(string="Margin less than limit requires approval %",
                                    related='company_id.at_least_margin',
                                    help="At lease margin after which approval of sale is required.")
    less_margin_approval = fields.Boolean(string="Force two levels of approvals",
                                    related='company_id.less_margin_approval',
                                    help="Provide a double validation mechanism for sale margin inferior than At Least Margin.")

    @api.onchange('company_id')
    def onchange_company_id(self):
        if self.company_id:
            company = self.company_id
            self.discount_approval = company.discount_approval
            self.limit_discount = company.limit_discount
            self.less_margin_approval = company.less_margin_approval
            self.at_least_margin = company.at_least_margin
            return super(AccountDiscountSettings, self).onchange_company_id()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: