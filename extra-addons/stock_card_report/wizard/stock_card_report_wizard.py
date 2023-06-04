# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval
import six


class StockCardReportWizard(models.TransientModel):
    _name = 'stock.card.report.wizard'
    _description = 'Stock Card Report Wizard'

    date_range_id = fields.Many2one(
        comodel_name='date.range',
        string='Period',
    )
    date_from = fields.Date(
        string='Start Date',
    )
    date_to = fields.Date(
        string='End Date',
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='Location',
        required=True,
    )
    product_ids = fields.Many2many(
        comodel_name='product.product',
        string='Products',
        required=True,
        default=lambda self: self._default_products()
    )

    def _default_products(self):
        context = self.env.context
        if context.get('active_ids') and context.get('active_model') \
                == 'product.product':
            product_ids = context['active_ids']
            return list(product_ids)

    @api.onchange('date_range_id')
    def _onchange_date_range_id(self):
        self.date_from = self.date_range_id.date_start
        self.date_to = self.date_range_id.date_end

    @api.multi
    def button_export_html(self):
        self.ensure_one()
        action = self.env.ref(
            'stock_card_report.action_report_stock_card_report_html')
        vals = action.read()[0]
        context = vals.get('context', {})
        if isinstance(context, six.string_types):
            context = safe_eval(context)
        model = self.env['report.stock.card.report']
        report = model.create(self._prepare_stock_card_report())
        context['active_id'] = report.id
        context['active_ids'] = report.ids
        vals['context'] = context
        return vals

    @api.multi
    def button_export_pdf(self):
        self.ensure_one()
        report_type = 'qweb-pdf'
        return self._export(report_type)

    @api.multi
    def button_export_xlsx(self):
        self.ensure_one()
        report_type = 'xlsx'
        return self._export(report_type)

    def _prepare_stock_card_report(self):
        self.ensure_one()
        return {
            'date_from': self.date_from,
            'date_to': self.date_to or fields.Date.context_today(self),
            'product_ids': [(6, 0, self.product_ids.ids)],
            'location_id': self.location_id.id,
        }

    def _export(self, report_type):
        model = self.env['report.stock.card.report']
        report = model.create(self._prepare_stock_card_report())
        return report.print_report(report_type)

# class product_product(models.Model):
#     _inherit= 'product.product'
#
#     @api.multi
#     def open_stock_card(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'name': 'Stock Card',
#             'view_type': 'form',
#             'view_mode': 'form',
#             'res_model': 'product.product',
#             'view_id': self.env.ref('stock_card_report.stock_card_report_from_product_action').id,
#             'create': False,
#             'target': 'new',
#         }