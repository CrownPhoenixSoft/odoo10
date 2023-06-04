# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, tools, _

class ProductCategory(models.Model):
    _inherit = "product.category"
    category_code = fields.Char('Internal Reference', index=True)