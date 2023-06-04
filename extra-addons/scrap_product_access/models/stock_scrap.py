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

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError


class stock_product_scrap(models.Model):
    _name = 'stock.scrap'
    _inherit = ['stock.scrap', 'mail.thread']

    message_ids = fields.One2many('mail.message', 'res_id', string='Messages', readonly=True)
    product_id = fields.Many2one('product.product', 'Product', required=False, states={'done': [('readonly', True)]},
                                 track_visibility='onchange')
    scrap_qty = fields.Float('Quantity', default=1.0, required=False, states={'done': [('readonly', True)]},
                             track_visibility='onchange')
    origin = fields.Char(string='Source Document', track_visibility='onchange')
    date_expected = fields.Datetime('Expected Date', default=fields.Datetime.now, track_visibility='onchange')
    state = fields.Selection([('draft', 'Draft'), ('waiting', 'Waiting'), ('done', 'Done'), ('reject', 'Reject')],
                             string='Status', default="draft", track_visibility='onchange')
    scrap_product_id = fields.One2many('scrap.product', 'stock_scrap_id', string='Scrap Product')
    product_uom_id = fields.Many2one('product.uom', 'Unit of Measure', required=False,
                                     states={'done': [('readonly', True)]})
    move_ids = fields.Many2many('stock.move', string='Stock Move', readonly=True)
    requested_by = fields.Many2one('res.users', string='Requested by')
    approved_by = fields.Many2one('res.users', string='Approved by')

    @api.multi
    def do_scrap(self):
        if self._context.get('is_confirmation'):
            if self.scrap_product_id:
                self.approved_by = self.env.uid
                move_list = []
                for scrap in self:
                    for each in scrap.scrap_product_id:
                        moves = scrap._get_origin_moves() or self.env['stock.move']
                        move = self.env['stock.move'].create(
                            scrap._prepare_move_values(each.product_id, each.product_uom_id, each.scrap_qty))
                        quants = self.env['stock.quant'].quants_get_preferred_domain(move.product_qty, move,
                                                                                     domain=[
                                                                                         ('qty', '>', 0),
                                                                                         (
                                                                                         'lot_id', '=', self.lot_id.id),
                                                                                         ('package_id', '=',
                                                                                          self.package_id.id)],
                                                                                     preferred_domain_list=scrap._get_preferred_domain())
                        if any([not x[0] for x in quants]):
                            raise UserError(_(
                                'You cannot scrap a move without having available stock for %s. You can correct it with an inventory adjustment.') % move.product_id.name)
                        self.env['stock.quant'].quants_reserve(quants, move)
                        move.action_done()
                        move_list.append(move.id)
                    scrap.write({'move_ids': [(6, 0, move_list)], 'state': 'done'})
                    moves.recalculate_move_state()
            else:
                raise UserError(_('Please select product first'))
        return True

    def _prepare_move_values(self, product, product_uom, qty):
        return {
            'name': self.name,
            'origin': self.origin or self.picking_id.name,
            'product_id': product.id,
            'product_uom': product_uom.id,
            'product_uom_qty': qty,
            'location_id': self.location_id.id,
            'location_dest_id': self.scrap_location_id.id,
            'restrict_lot_id': self.lot_id.id,
            'restrict_partner_id': self.owner_id.id,
            'picking_id': self.picking_id.id
        }

    @api.multi
    def action_get_stock_moves(self):
        action = self.env.ref('stock.stock_move_action').read([])[0]
        moves = self.mapped('move_ids')
        action['domain'] = [('id', 'in', moves.ids)]
        return action

    @api.multi
    def do_waiting(self):
        if self.scrap_product_id:
            self.requested_by = self.env.uid
            self.state = 'waiting'
        else:
            raise UserError(_('Please select product first'))

    @api.multi
    def do_reject(self):
        self.state = 'reject'

    @api.multi
    def do_draft(self):
        self.state = 'draft'


class scrap_product(models.Model):
    _name = 'scrap.product'

    stock_scrap_id = fields.Many2one('stock.scrap', string='Scrap Id')
    product_uom_id = fields.Many2one('product.uom', 'Unit of Measure', required=True)
    #     states = fields.Selection([('draft', 'Draft'),('done', 'Done')],realated='stock_scrap_id.state', string = 'state')
    product_id = fields.Many2one('product.product', 'Product', required=True, track_visibility='onchange')
    scrap_qty = fields.Float('Quantity', default=1.0, required=True, track_visibility='onchange')

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id

class StockScrapReport(models.AbstractModel):
    _name = 'report.scrap_product_access.report_stock_scrap'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('scrap_product_access.report_stock_scrap')
        
        docargs = {
            'doc_ids': self.env["stock.scrap"].browse(docids[0]),
            'doc_model': report.model,
            'docs': self,
        }
        return report_obj.render('scrap_product_access.report_stock_scrap', docargs)