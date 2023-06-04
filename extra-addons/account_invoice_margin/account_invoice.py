# -*- coding: utf-8 -*-
# © 2015-2017 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api
import odoo.addons.decimal_precision as dp


class AccountInvoiceLine(models.Model):
    _inherit = 'account.invoice.line'

    standard_price_company_currency = fields.Float(
        string='Cost Price in Company Currency', readonly=True,
        digits=dp.get_precision('Product Price'),
        help="Cost price in company currency in the unit of measure "
        "of the invoice line (which may be different from the unit "
        "of measure of the product).")
    standard_price_invoice_currency = fields.Float(
        string='Cost Price in Invoice Currency', readonly=True,
        compute='_compute_margin', store=True,
        digits=dp.get_precision('Product Price'),
        help="Cost price in invoice currency in the unit of measure "
        "of the invoice line")
    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency', readonly=True, store=True,
        compute='_compute_margin', currency_field='company_currency_id')
    margin_rate = fields.Float(
        string="Margin Rate", readonly=True, store=True,
        compute='_compute_margin',
        digits=(16, 2), help="Margin rate in percentage of the sale price")

    @api.depends(
        'standard_price_company_currency', 'invoice_id.currency_id',
        'invoice_id.type', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'quantity', 'price_subtotal')
    def _compute_margin(self):
        for il in self:
            standard_price_inv_cur = 0.0
            if il.product_id:
                standard_price_inv_cur = il.product_id.standard_price
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            margin_rate = 0.0
            inv = il.invoice_id
            if inv and inv.type in ('out_invoice', 'out_refund'):
                # it works in _get_current_rate
                # even if we set date = False in context
                # standard_price_inv_cur is in the UoM of the invoice line
                if il.product_id.uom_id != il.uom_id:
                    standard_price_invoice =\
                        inv.company_id.currency_id.with_context(
                            date=inv.date_invoice).compute(standard_price_inv_cur,inv.currency_id)
                    standard_price_inv_cur = il.product_id.uom_id._compute_price(standard_price_invoice,il.uom_id)
                    margin_inv_cur = il.price_subtotal - il.quantity * standard_price_inv_cur
                    margin_comp_cur = inv.currency_id.with_context(date=inv.date_invoice).compute(margin_inv_cur, inv.company_id.currency_id)
                    if il.price_subtotal:
                        margin_rate = 100 * margin_inv_cur / il.price_subtotal
#                         margin_rate = il.product_id.uom_id._compute_price(margin_rate_old,il.uom_id)
                    # for a refund, margin should be negative
                    # but margin rate should stay positive
                    if inv.type == 'out_refund':
                        margin_inv_cur *= -1
                        margin_comp_cur *= -1
                else:
                    standard_price_inv_cur =\
                        inv.company_id.currency_id.with_context(
                            date=inv.date_invoice).compute(
                                standard_price_inv_cur,
                                inv.currency_id)
                    margin_inv_cur = il.price_subtotal - il.quantity * standard_price_inv_cur
                    margin_comp_cur = inv.currency_id.with_context(date=inv.date_invoice).compute(margin_inv_cur, inv.company_id.currency_id)
                    if il.price_subtotal:
                        margin_rate = 100 * margin_inv_cur / il.price_subtotal
                    # for a refund, margin should be negative
                    # but margin rate should stay positive
                    if inv.type == 'out_refund':
                        margin_inv_cur *= -1
                        margin_comp_cur *= -1
            il.standard_price_invoice_currency = standard_price_inv_cur
            il.margin_invoice_currency = margin_inv_cur
            il.margin_company_currency = margin_comp_cur
            il.margin_rate = margin_rate

    # We want to copy standard_price on invoice line for customer
    # invoice/refunds. We can't do that via on_change of product_id,
    # because it is not always played when invoice is created from code
    # => we inherit write/create
    # We write standard_price_company_currency even on supplier invoice/refunds
    # because we don't have access to the 'type' of the invoice
    @api.model
    def create(self, vals):
        if vals.get('product_id'):
            pp = self.env['product.product'].browse(vals['product_id'])
            std_price = pp.standard_price
            inv_uom_id = vals.get('uom_id')
            uom_id = self.env['product.uom'].search([('id', '=', inv_uom_id)])
            if inv_uom_id and inv_uom_id != pp.uom_id.id:
                std_price = pp.uom_id._compute_price(std_price,uom_id)
            vals['standard_price_company_currency'] = std_price
        return super(AccountInvoiceLine, self).create(vals)
    

    @api.multi
    def write(self, vals):
        if not vals:
            vals = {}
        if 'product_id' in vals or 'uom_id' in vals:
            for il in self:
                if 'product_id' in vals:
                    if vals.get('product_id'):
                        pp = self.env['product.product'].browse(
                            vals['product_id'])
                    else:
                        pp = False
                else:
                    pp = il.product_id or False
                # uom_id is NOT a required field
                if 'uom_id' in vals:
                    if vals.get('uom_id'):
                        inv_uom = self.env['product.uom'].browse(
                            vals['uom_id'])
                    else:
                        inv_uom = False
                else:
                    inv_uom = il.uom_id or False
                std_price = 0.0
                if pp:
                    std_price = pp.standard_price
                    if inv_uom and inv_uom != pp.uom_id:
                        std_price = pp.uom_id._compute_price(
                            std_price, inv_uom)
                il.write({'standard_price_company_currency': std_price})
        return super(AccountInvoiceLine, self).write(vals)


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    margin_invoice_currency = fields.Monetary(
        string='Margin in Invoice Currency',
        readonly=True, compute='_compute_margin', store=True,
        currency_field='currency_id')
    margin_company_currency = fields.Monetary(
        string='Margin in Company Currency',
        readonly=True, compute='_compute_margin', store=True,
        currency_field='company_currency_id')

    @api.depends(
        'type',
        'invoice_line_ids.margin_invoice_currency',
        'invoice_line_ids.margin_company_currency')
    def _compute_margin(self):
        for inv in self:
            margin_inv_cur = 0.0
            margin_comp_cur = 0.0
            if inv.type in ('out_invoice', 'out_refund'):
                for il in inv.invoice_line_ids:
                    margin_inv_cur += il.margin_invoice_currency
                    margin_comp_cur += il.margin_company_currency
            inv.margin_invoice_currency = margin_inv_cur
            inv.margin_company_currency = margin_comp_cur
            
class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"
    
    margin_company_currency = fields.Monetary(string = 'Margin Company Currency')
    
    
    def _select(self):
        select_str = """
            SELECT sub.id, sub.date, sub.product_id, sub.partner_id, sub.country_id, sub.account_analytic_id,
                sub.payment_term_id, sub.uom_name, sub.currency_id, sub.journal_id,
                sub.fiscal_position_id, sub.user_id, sub.company_id, sub.nbr, sub.type, sub.state,
                sub.weight, sub.volume,
                sub.categ_id, sub.date_due, sub.account_id, sub.account_line_id, sub.partner_bank_id,
                sub.product_qty, sub.price_total as price_total, sub.price_average as price_average,
                sub.margin_company_currency,
                COALESCE(cr.rate, 1) as currency_rate, sub.residual as residual, sub.commercial_partner_id as commercial_partner_id
        """
        return select_str
    
    def _sub_select(self):
        select_str = """
                SELECT ail.id AS id,
                    ai.date_invoice AS date,
                    ail.product_id, ai.partner_id, ai.payment_term_id, ail.account_analytic_id,
                    u2.name AS uom_name,
                    ai.currency_id, ai.journal_id, ai.fiscal_position_id, ai.user_id, ai.company_id,
                    1 AS nbr,
                    ai.type, ai.state, pt.categ_id, ai.date_due, ai.account_id, ail.account_id AS account_line_id,
                    ai.partner_bank_id,
                    sum(ail.margin_company_currency) as margin_company_currency,
                    SUM ((invoice_type.sign * ail.quantity) / u.factor * u2.factor) AS product_qty,
                    SUM(ail.price_subtotal_signed * invoice_type.sign) AS price_total,
                    SUM(ABS(ail.price_subtotal_signed)) / CASE
                            WHEN SUM(ail.quantity / u.factor * u2.factor) <> 0::numeric
                               THEN SUM(ail.quantity / u.factor * u2.factor)
                               ELSE 1::numeric
                            END AS price_average,
                    ai.residual_company_signed / (SELECT count(*) FROM account_invoice_line l where invoice_id = ai.id) *
                    count(*) * invoice_type.sign AS residual,
                    ai.commercial_partner_id as commercial_partner_id,
                    partner.country_id,
                    SUM(pr.weight * (invoice_type.sign*ail.quantity) / u.factor * u2.factor) AS weight,
                    SUM(pr.volume * (invoice_type.sign*ail.quantity) / u.factor * u2.factor) AS volume
                    """
        return select_str