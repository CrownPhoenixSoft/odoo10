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

class ProductMargin(models.TransientModel):
    _inherit = 'product.margin'

    user_id = fields.Many2one('res.users', string = 'SalePerson')
    
    
    @api.multi
    def action_open_window(self):
        self.ensure_one()
        context = dict(self.env.context or {})

        def ref(module, xml_id):
            proxy = self.env['ir.model.data']
            return proxy.get_object_reference(module, xml_id)

        model, search_view_id = ref('product', 'product_search_form_view')
        model, graph_view_id = ref('product_margin', 'view_product_margin_graph')
        model, form_view_id = ref('product_margin', 'view_product_margin_form')
        model, tree_view_id = ref('product_margin', 'view_product_margin_tree')

        context.update(invoice_state=self.invoice_state)
        if self.user_id:
            context.update(user_id = self.user_id.id)

        if self.from_date:
            context.update(date_from=self.from_date)

        if self.to_date:
            context.update(date_to=self.to_date)

        views = [
            (tree_view_id, 'tree'),
            (form_view_id, 'form'),
            (graph_view_id, 'graph')
        ]
        return {
            'name': _('Product Margins'),
            'context': context,
            'view_type': 'form',
            "view_mode": 'tree,form,graph',
            'res_model': 'product.product',
            'type': 'ir.actions.act_window',
            'views': views,
            'view_id': False,
            'search_view_id': search_view_id,
        }

