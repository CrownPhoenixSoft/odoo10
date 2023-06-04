# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 GRIMMETTE,LLC <info@grimmette.com>

import base64
from datetime import datetime
from tempfile import TemporaryFile
from odoo import api, fields, models, tools, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT
from odoo.exceptions import UserError, ValidationError
from __builtin__ import str
class ProductPricelistExcel(models.Model):
    '''
    Configuration Pricelists Excel
    '''
    _name = "product.pricelist_excel"
    _description = "Pricelist Excel"
    _disallowed_datetime_patterns = tools.DATETIME_FORMATS_MAP.keys()
    _disallowed_datetime_patterns.remove('%y')
    name = fields.Char(string='Name', required=True)
    pricelist_id = fields.Many2one('product.pricelist', string='Pricelist Name', required=True)
    active = fields.Boolean(string='Active', help="If unchecked, it will allow you to hide the pricelist without removing it.", default=True)
    out_file_name = fields.Char(string='File Name', default='pricelist_%d-%m-%Y.xlsx', help="The file name of the price list. See bellow Legends for supported Date and Time Formats.")
    data = fields.Binary('Template Header', attachment=True)
    doc_count = fields.Integer(compute='_compute_attached_docs_count', string="Number of documents attached")
    datas_fname = fields.Char(compute='_compute_attached_doc_name', string='File Name')
    template_name_id = fields.Many2one(comodel_name="ir.attachment", string="Template", required=False,
                                   help="This field holds the Excel pricelist template used for the this pricelist. You must upload the template files.",
                                   domain = "[('res_model', '=', 'product.pricelist_excel'), ('res_id', '=', id)]"
                                   )
    description = fields.Text('Description')
    sheet_reference = fields.Char('Sheet Price', required=True, default='Sheet1', help="Sheet name, for example Sheet5, Price List, etc. The sheet name must match the sheet name in the template file.") 
    header_reference = fields.Char('Header Location', help="Header Location. Format e.g. A6:R6", required=True, default='A6:R6')
    qty_reference = fields.Char('QTY Cells Location', help="QTY:1-5 Data Cells Location. Format e.g. D7:H7", required=True, default='D7:H7')
    company_bool = fields.Boolean('Company Name', default=True) 
    price_name_bool = fields.Boolean('Pricelist Name', default=True) 
    currency_bool = fields.Boolean('Currency', default=True) 
    print_date_bool = fields.Boolean('Print Date', default=True) 
    company_reference = fields.Char('Cell', help="Location of the Company Name Cell. Format e.g. A7", required=True, default='A1') 
    price_name_reference = fields.Char('Cell', help="Location of the Pricelist Name Cell. Format e.g. A7", required=True, default='E3') 
    currency_reference = fields.Char('Cell', help="Location of the Currency Cell. Format e.g. A7", required=True, default='R4') 
    print_date_reference = fields.Char('Cell', help="Location of the Print Date Cell. Format e.g. A7", required=True, default='R5') 
    product_code_bool = fields.Boolean('Product Code', default=True, readonly=True)
    product_name_bool = fields.Boolean('Name', default=True, readonly=True)
    attributes_bool = fields.Boolean('Attributes', default=True)
    vat_bool = fields.Boolean('Taxes', default=True) 
    uom_bool = fields.Boolean('UOM', default=True) 
    qty_case_bool = fields.Boolean('QTY/Case', default=True) 
    onhand_bool = fields.Boolean('On Hand', default=True) 
    hscode_bool = fields.Boolean('HS Code', default=True) 
    ean_bool = fields.Boolean('EAN', default=True) 
    weight_bool = fields.Boolean('Weight', default=True) 
    volume_bool = fields.Boolean('Volume', default=True) 
    description_bool = fields.Boolean('Description', help="Description for Quotations", default=True) 
    customer_lead_time_bool = fields.Boolean('Delivery Time', help="Customer Lead Time", default=True) 
    product_code_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='A7')
    product_name_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='B7')
    attributes_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='C7')
    vat_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='I7')
    uom_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='J7')
    qty_case_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='K7')
    onhand_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='L7')
    hscode_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='M7')
    ean_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='N7')
    weight_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='O7')
    volume_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='P7')
    description_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='Q7')
    customer_lead_time_cell_reference = fields.Char('First Cell', help="The first cell of data in a column. Format e.g. A7", required=True, default='R7')
    show_categories = fields.Boolean('Categories', default=True)
    category_style = fields.Selection([
        ('0', 'White, Background 1'),
        ('1', 'Black, Text 1'),
        ('2', 'Gray-25%, Background 2'),
        ('3', 'Blue-Gray, Text 2'),
        ('4', 'Blue, Accent 1'),
        ('5', 'Orange, Accent 2'),
        ('6', 'Gray-50%, Accent 3'),
        ('7', 'Gold, Accent 4'),
        ('8', 'Blue, Accent 5'),
        ('9', 'Green, Accent 6'),
    ], string='Colors', required=True, default='4',
        help="The Excel Theme Colors for Category.")
    show_categories_code = fields.Boolean('Categories Code', default=False)
    show_level = fields.Boolean('Row Level', default=True)
    show_autofilter = fields.Boolean('Autofilter', default=True)
    show_images = fields.Boolean('Images', default=False)
    wraptxt = fields.Boolean('Wrap Text', default=False)
    @api.multi
    def attachment_doc_view(self):
        self.ensure_one()
        domain = [
            '&', ('res_model', '=', self._name), ('res_id', 'in', self.ids)]
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Excel pricelist header templates.</p><p>
                        Prepare and upload the file in MS Excel format 
                        containing a header template for the pricelist.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
    def _compute_attached_docs_count(self):
        Attachment = self.env['ir.attachment']
        for doc in self:
            doc.doc_count = Attachment.search_count([
                '&', ('res_model', '=', 'product.pricelist_excel'), ('res_id', '=', doc.id)
            ])
    @api.model
    @api.depends('data')
    def _compute_attached_doc_name(self):
        Attachment = self.env['ir.attachment']
        datafile = Attachment.search_read([
            '&', ('res_model', '=', 'product.pricelist_excel'), ('res_id', '=', self.id), ('res_field', '=', 'data')
            ])
        if datafile:
            return datafile[0]['datas_fname']
    @api.constrains('out_file_name')
    def _check_format(self):
        for lang in self:
            for pattern in lang._disallowed_datetime_patterns:
                if (lang.out_file_name and pattern in lang.out_file_name):
                    raise ValidationError(_('Invalid date/time format directive specified. '
                                            'Please refer to the list of allowed directives.'))
