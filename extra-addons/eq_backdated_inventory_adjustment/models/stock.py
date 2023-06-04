# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import models, fields


class Stock_Move(models.Model):
    _inherit = 'stock.move'

    def action_done(self):
        res = super(Stock_Move, self).action_done()
        for each_move in self:
            if each_move.inventory_id and each_move.inventory_id.is_backdated_inv:
                each_move.write(
                    {'date':each_move.inventory_id.inv_backdated or fields.Datetime.now(),
                    'date_expected':each_move.inventory_id.inv_backdated or fields.Datetime.now(),
                    'note':each_move.inventory_id.backdated_remark, 'origin':each_move.inventory_id.backdated_remark})
#                 each_move.move_line_ids.write(
#                     {'date':each_move.inventory_id.inv_backdated or fields.Datetime.now()})
        return res


class stock_inventory(models.Model):
    _inherit = 'stock.inventory'

    is_backdated_inv = fields.Boolean(string="Is Backdated Inventory?",copy=False)
    inv_backdated = fields.Date(string="Inventory Backdate",copy=False)
    backdated_remark = fields.Char(string="Notes",copy=False)

    def post_inventory(self):
        for inventory in self:
            date = inventory.accounting_date or inventory.date
            if inventory.is_backdated_inv:
                date = inventory.inv_backdated
        return super(stock_inventory, inventory.with_context(force_period_date=date)).post_inventory()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: