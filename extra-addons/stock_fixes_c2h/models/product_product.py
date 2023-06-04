# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models,fields


class Product(models.Model):
    _inherit = "product.product"

    def pending_stock_moves(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Pending Stock Move',
            'view_mode': 'tree',
            'res_model': 'stock.move',
            'domain': [('product_id', '=', self.id), ('state', 'not in', ['cancel', 'done'])],
            'context': "{'create': False}"
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4
