# Copyright 2019 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models

class stock_move(models.Model):
    _inherit= 'stock.move'

    reference = fields.Char(string = 'Reference', related='picking_id.name', store=True)
    partner_name = fields.Char(string= 'Partner', related='partner_id.name', store=True)
    user_name = fields.Char(string='User', related='create_uid.name', store=True)
    vendor_name = fields.Char(string = 'Partner', related='picking_partner_id.name', store=True)

class StockCardView(models.TransientModel):
    _name = 'stock.card.view'
    _description = 'Stock Card View'
    _order = 'date'

    date = fields.Datetime()
    product_id = fields.Many2one(comodel_name='product.product')
    product_qty = fields.Float()
    product_uom_qty = fields.Float()
    product_uom = fields.Many2one(comodel_name='uom.uom')
    reference = fields.Char()
    partner_name = fields.Char()
    user_name = fields.Char()
    location_id = fields.Many2one(comodel_name='stock.location')
    location_dest_id = fields.Many2one(comodel_name='stock.location')
    is_initial = fields.Boolean()
    product_in = fields.Float()
    product_out = fields.Float()


class StockCardReport(models.TransientModel):
    _name = 'report.stock.card.report'
    _description = 'Stock Card Report'

    # Filters fields, used for data computation
    date_from = fields.Date()
    date_to = fields.Date()
    product_ids = fields.Many2many(
        comodel_name='product.product',
    )
    location_id = fields.Many2one(
        comodel_name='stock.location',
    )

    # Data fields, used to browse report data
    results = fields.Many2many(
        comodel_name='stock.card.view',
        compute='_compute_results',
        help='Use compute fields, so there is nothing store in database',
    )

    @api.multi
    def _compute_results(self):
        self.ensure_one()
        date_from = self.date_from or '0001-01-01'
        self.date_to = self.date_to or fields.Date.context_today(self)
        locations = self.env['stock.location'].search(
            [('id', 'child_of', [self.location_id.id])])
        self._cr.execute("""
            SELECT move.date, move.product_id, move.product_qty,move.partner_name,move.user_name,move.vendor_name,
                move.product_uom_qty, move.product_uom, move.reference,move.origin,move.name,
                move.location_id, move.location_dest_id,
                case when move.location_dest_id in %s
                    then move.product_qty end as product_in,
                case when move.location_id in %s
                    then move.product_qty end as product_out,
                case when move.date < %s then True else False end as is_initial
            FROM stock_move move
            WHERE (move.location_id in %s or move.location_dest_id in %s)
                and move.state = 'done' and move.product_id in %s
                and CAST(move.date AS date) <= %s
            ORDER BY move.date, move.reference,move.origin,move.name,move.partner_name,move.user_name,move.vendor_name
        """, (
            tuple(locations.ids), tuple(locations.ids), date_from,
            tuple(locations.ids), tuple(locations.ids),
            tuple(self.product_ids.ids), self.date_to))
        stock_card_results = self._cr.dictfetchall()
        for data in stock_card_results:
            if not data.get('partner_name'):
                data.update({'partner_name':data.get('vendor_name')})
            if data.get('reference') and data.get('origin'):
                data.update({'reference':data.get('reference')+'-'+data.get('origin')})
            elif not data.get('reference'):
                data.update({'reference':data.get('name')})

        ReportLine = self.env['stock.card.view']
        self.results = [ReportLine.new(line).id for line in stock_card_results]

    @api.multi
    def _get_initial(self, product_line):
        product_input_qty = sum(product_line.mapped('product_in'))
        product_output_qty = sum(product_line.mapped('product_out'))
        return product_input_qty - product_output_qty

    @api.multi
    def print_report(self, report_type='qweb'):
        self.ensure_one()
        # active_ids = self.env.context.get('active_ids', [])
        if report_type == 'xlsx':
            report_name = 'stock_card_report.report_stock_card_report_xlsx'
        else:
            report_name = 'stock_card_report.report_stock_card_report_pdf'
            print("\n\n\n------report_name----.>>>>>>>>",report_name)
        return self.env['report'].get_action(docids=self.ids,
                                             report_name=report_name)

    def _get_html(self):
        result = {}
        rcontext = {}
        report = self.browse(self._context.get('active_id'))
        if report:
            rcontext['o'] = report
            result['html'] = self.env.ref(
                'stock_card_report.report_stock_card_report_html').render(
                    rcontext)
        return result

    @api.model
    def get_html(self, given_context=None):
        return self.with_context(given_context)._get_html()
