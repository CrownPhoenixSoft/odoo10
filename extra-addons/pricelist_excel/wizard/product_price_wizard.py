# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

import threading
import logging
from email import _name
_logger = logging.getLogger(__name__)
class PriceListExcelWizard(models.TransientModel):
    _name = 'price_list_excel.wizard'
    _description = "Price List Wizard"
    pricelist_conf = fields.Many2one('product.pricelist_excel', 'PriceList Excel', required=True, ondelete='cascade')
    qty1 = fields.Integer('Quantity-1', default=1)
    qty2 = fields.Integer('Quantity-2', default=5)
    qty3 = fields.Integer('Quantity-3', default=10)
    qty4 = fields.Integer('Quantity-4', default=0)
    qty5 = fields.Integer('Quantity-5', default=0)
    @api.multi
    def export_excel(self):
        """
        To get the data and export
        @return : return file
        """
        datas = {'ids': self.env.context.get('active_ids', [])}
        res = self.read(['pricelist_conf', 'qty1', 'qty2', 'qty3', 'qty4', 'qty5'])
        res = res and res[0] or {}
        res['pricelist_conf_id'] = res['pricelist_conf'][0]
        datas['form'] = res
        return self.env['pricelist_excel_gen'].create_xls(datas)
