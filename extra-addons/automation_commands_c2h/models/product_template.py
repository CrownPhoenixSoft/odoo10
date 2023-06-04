# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def archive_reordering_rules_and_produces(self):
        for record in self._context.get('active_ids'):
            current_record = self.browse(record)
            products = current_record.mapped('product_variant_ids')
            current_order_reordering_rules = self.env['stock.warehouse.orderpoint'].search([ ('product_id', 'in', products.ids) ])
            if current_order_reordering_rules:
                for item in current_order_reordering_rules:
                    item.toggle_active()
                current_record.toggle_active()
