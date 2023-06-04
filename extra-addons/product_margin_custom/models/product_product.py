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
import time
from odoo import models, fields, api, _

class ProductProduct(models.Model):
    _inherit = "product.product"
    
    user_id = fields.Many2one('res.users', string='SalePerson', compute='_compute_product_margin_fields_values', store=False)
    
    def _compute_product_margin_fields_values(self, field_names=None):
        res = {}
        if field_names is None:
            field_names = []
        for val in self:
            res[val.id] = {}
            date_from = self.env.context.get('date_from', time.strftime('%Y-01-01'))
            date_to = self.env.context.get('date_to', time.strftime('%Y-12-31'))
            invoice_state = self.env.context.get('invoice_state', 'open_paid')
            user_id = self.env.context.get('user_id')
            
            res[val.id]['date_from'] = date_from
            res[val.id]['date_to'] = date_to
            res[val.id]['invoice_state'] = invoice_state
            res[val.id]['user_id'] = user_id
            invoice_types = ()
            states = ()
            if invoice_state == 'paid':
                states = ('paid',)
            elif invoice_state == 'open_paid':
                states = ('open', 'paid')
            elif invoice_state == 'draft_open_paid':
                states = ('draft', 'open', 'paid')
            if "force_company" in self.env.context:
                company_id = self.env.context['force_company']
            else:
                company_id = self.env.user.company_id.id

            # Cost price is calculated afterwards as it is a property
            sqlstr = """
                select
                    sum(l.price_unit * l.quantity)/nullif(sum(l.quantity),0) as avg_unit_price,
                    sum(l.quantity) as num_qty,
                    sum(l.quantity * (l.price_subtotal/(nullif(l.quantity,0)))) as total,
                    sum(l.quantity * pt.list_price) as sale_expected
                from account_invoice_line l
                left join account_invoice i on (l.invoice_id = i.id)
                left join product_product product on (product.id=l.product_id)
                left join product_template pt on (pt.id = product.product_tmpl_id)
                where l.product_id = %s and i.state in %s and i.type IN %s and (i.date_invoice IS NULL or (i.date_invoice>=%s and i.date_invoice<=%s and i.company_id=%s))
                and i.user_id = %s
                """
            invoice_types = ('out_invoice', 'in_refund')
            self.env.cr.execute(sqlstr, (val.id, states, invoice_types, date_from, date_to, company_id, user_id))
            result = self.env.cr.fetchall()[0]
            res[val.id]['sale_avg_price'] = result[0] and result[0] or 0.0
            res[val.id]['sale_num_invoiced'] = result[1] and result[1] or 0.0
            res[val.id]['turnover'] = result[2] and result[2] or 0.0
            res[val.id]['sale_expected'] = result[3] and result[3] or 0.0
            res[val.id]['sales_gap'] = res[val.id]['sale_expected'] - res[val.id]['turnover']
            ctx = self.env.context.copy()
            ctx['force_company'] = company_id
            invoice_types = ('in_invoice', 'out_refund')
            self.env.cr.execute(sqlstr, (val.id, states, invoice_types, date_from, date_to, company_id, user_id))
            result = self.env.cr.fetchall()[0]
#             print  "\n\n- -result---", result
            res[val.id]['purchase_avg_price'] = result[0] and result[0] or 0.0
            res[val.id]['purchase_num_invoiced'] = result[1] and result[1] or 0.0
            res[val.id]['total_cost'] = result[2] and result[2] or 0.0
            res[val.id]['normal_cost'] = val.standard_price * res[val.id]['purchase_num_invoiced']
            res[val.id]['purchase_gap'] = res[val.id]['normal_cost'] - res[val.id]['total_cost']

            res[val.id]['total_margin'] = res[val.id]['turnover'] - res[val.id]['total_cost']
            res[val.id]['expected_margin'] = res[val.id]['sale_expected'] - res[val.id]['normal_cost']
            res[val.id]['total_margin_rate'] = res[val.id]['turnover'] and res[val.id]['total_margin'] * 100 / res[val.id]['turnover'] or 0.0
            res[val.id]['expected_margin_rate'] = res[val.id]['sale_expected'] and res[val.id]['expected_margin'] * 100 / res[val.id]['sale_expected'] or 0.0
            
            
            for k, v in res[val.id].items():
                setattr(val, k, v)
        return res
    
    
    
