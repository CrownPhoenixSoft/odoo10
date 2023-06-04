# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

import base64
from cStringIO import StringIO
from odoo import api, fields, models
try:
    import xlwt
except ImportError:
    xlwt = None

class sale_day_book_wizard(models.TransientModel):
    _name = "sale.day.book.wizard"
    
    start_date = fields.Date('Start Period', required=True)
    end_date = fields.Date('End Period', required=True)
    warehouse = fields.Many2many('stock.warehouse', 'wh_wiz_rel', 'wh', 'wiz', string='Warehouse',required=True)
    category = fields.Many2many('product.category', 'categ_wiz_rel', 'categ', 'wiz')
    location_id = fields.Many2one('stock.location', string= 'Location')
    company_id = fields.Many2one('res.company', string= 'Company')
    display_sum = fields.Boolean("Summary")
    
    

    @api.multi  
    def print_report(self,data):
        datas = {
            'ids': self._ids,
            'model': 'sales.day.book.wizard',
            'start_date':self.start_date,
            'end_date':self.end_date,
            'warehouse':self.get_warehouse(),
            'company_id':self.get_company(),
            'display_sum':self.display_sum,
            'category':self.get_cat(),
            }
        return self.env['report'].get_action(self, 'bi_inventory_valuation_reports.sales_daybook_template', data=datas)
    
    def get_warehouse(self):
        if self.warehouse:
            l1 = []
            l2 = []
            for i in self.warehouse:
                obj = self.env['stock.warehouse'].search([('id', '=', i.id)])
                for j in obj:
                    l2.append(j.id)
            return l2
        return []

    def get_cat(self):
        if self.category:
            l1 = []
            l2 = []
            for i in self.category:
                obj = self.env['product.category'].search([('id', '=', i.id)])
                for j in obj:
                    l2.append(j.id)
            return l2
        return []
    
    def _get_warehouse_name(self):
        if self.warehouse:
            l1 = []
            l2 = []
            for i in self.warehouse:
                obj = self.env['stock.warehouse'].search([('id', '=', i.id)])
                l1.append(obj.name)
                myString = ",".join(l1 )
            return myString
        return ''


    def get_company(self):
        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.name)
            return l1

    def get_currency(self):
        if self.company_id:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('id', '=', self.company_id.id)])
            l1.append(obj.currency_id.name)
            return l1

    def get_category(self):
        if self.category:
            l2 = []
            obj = self.env['product.category'].search([('id', 'in', self.category)])
            for j in obj:
                l2.append(j.id)
            return l2
        return ''
    
    def get_date(self):
        date_list = []
        obj = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date)])
        for j in obj:
            date_list.append(j.id)
        return date_list

    def get_lines(self, warehouse):
        lines = []
        loc_list = []
        type_list = []
        beginning = 0
        cat_list=[]
        stock_history = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date)])
        if self.company_id:
            stock_history = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date),('company_id', '=', self.company_id.id)])
        if self.category:
            for cat in self.category:
                cat_list.append(cat.id)
            stock_history = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date),('product_categ_id', 'in', cat_list)])
        if self.category and self.company_id:
            for cat in self.category:
                cat_list.append(cat.id)
            stock_history = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date),('product_categ_id', 'in', cat_list),('company_id', '=', self.company_id.id)])
        stock_list = []
        product_list = []
        for i in stock_history:
            if i.product_id.id not in product_list:
                product_list.append(i.product_id.id)
        for pro in product_list:
            sale_value = 0
            purchase_value = 0
            internal = 0
            beginning = 0
            product = self.env['product.product'].browse(pro)
            sale_obj = self.env['sale.order.line'].search([('order_id.state', 'in', ('sale', 'done')),
                                                           ('product_id', '=', product.id),
                                                           ('order_id.warehouse_id', '=', warehouse)])
            for i in sale_obj:
                sale_value = sale_value + i.product_uom_qty
            purchase_obj = self.env['purchase.order.line'].search([('order_id.state', 'in', ('purchase', 'done')),
                                                                   ('product_id', '=', product.id),
                                                                   ('order_id.picking_type_id', '=', warehouse)])
            for i in purchase_obj:
                purchase_value = purchase_value + i.product_qty
            stock_inv_line_obj = self.env['stock.inventory.line']
            stock_loc_obj = self.env['stock.location'].search([('usage','=','internal')])
            for j in stock_loc_obj:
                loc_list.append(j.id)
            stock_inv_lines = stock_inv_line_obj.search([('product_id', '=', product.id),('location_id', 'in', loc_list)])
            for b in stock_inv_lines:
                beginning = b.product_qty
            stock_pick_type_obj = self.env['stock.picking.type'].search([('code','=','internal')])
            for k in stock_pick_type_obj:
                type_list.append(k.id)
            stock_pick_obj = self.env['stock.picking']
            stock_pick_lines = stock_pick_obj.search([('picking_type_id', 'in', type_list)])
            for b in stock_inv_lines:
                beginning = b.product_qty
            for move_line in stock_pick_lines:
                for move in move_line:
                    if move.product_id == product.id:
                        internal = move.product_uom_qty
            available_qty = product.with_context({'warehouse': warehouse}).virtual_available + \
                            product.with_context({'warehouse': warehouse}).outgoing_qty - \
                            product.with_context({'warehouse': warehouse}).incoming_qty
            value = available_qty * product.standard_price
            vals = {
                'sku': product.default_code,
                'name': product.name,
                'category': product.categ_id.name,
                'cost_price': product.standard_price,
                'available': available_qty,
                'virtual': product.with_context({'warehouse': warehouse}).virtual_available,
                'incoming': product.with_context({'warehouse': warehouse}).incoming_qty,
                'outgoing': product.with_context({'warehouse': warehouse}).outgoing_qty,
                'net_on_hand': product.with_context({'warehouse': warehouse}).qty_available,
                'total_value': value,
                'sale_value': sale_value,
                'purchase_value': purchase_value,
                'beginning':beginning,
                'internal':internal,
            }
            lines.append(vals)
        return lines

    def get_data(self):
        lines = []
        cat_list=[]
        category_obj = self.env['product.category']
        category_ids = category_obj.search([])
        lines = []
        loc_list = []
        type_list = []
        sale_value = 0
        purchase_value = 0
        internal = 0
        internal_cat = 0
        beginning = 0
        if self.warehouse:
            l1 = []
            l2 = []
            for i in self.warehouse:
                l1.append(i.id)
        for c in category_ids:
            cat_list.append(c.id)
        stock_history = self.env['stock.history'].search([('date', '>=', self.start_date),('date', '<=', self.end_date),('product_categ_id', 'in', cat_list)])
        stock_list = []
        product_list = []
        for i in stock_history:
            if i.product_id.id not in product_list:
                product_list.append(i.product_id.id)
        for catgory_product in product_list:
            product = self.env['product.product'].browse(catgory_product)
            sale_obj = self.env['sale.order.line'].search([('order_id.state', 'in', ('sale', 'done')),
                                                   ('product_id', '=', catgory_product),
                                                   ('order_id.warehouse_id', 'in', l1)])
            if sale_obj:
                for i in sale_obj:
                    sale_value = sale_value + i.product_uom_qty
            purchase_obj = self.env['purchase.order.line'].search([('order_id.state', 'in', ('purchase', 'done')),
                                                           ('product_id', '=', catgory_product),
                                                           ('order_id.picking_type_id', 'in', l1)])
            if purchase_obj:
                for i in purchase_obj:
                    purchase_value = purchase_value + i.product_qty
            stock_inv_line_obj = self.env['stock.inventory.line']
            stock_loc_obj = self.env['stock.location'].search([('usage','=','internal')])
            for j in stock_loc_obj:
                loc_list.append(j.id)
            stock_inv_lines = stock_inv_line_obj.search([('product_id', '=', catgory_product),('location_id', 'in', loc_list)])
            for b in stock_inv_lines:
                beginning = b.product_qty
            stock_pick_type_obj = self.env['stock.picking.type'].search([('code','=','internal')])
            for k in stock_pick_type_obj:
                type_list.append(k.id)
            stock_pick_obj = self.env['stock.picking']
            stock_pick_lines = stock_pick_obj.search([('picking_type_id', 'in', type_list)])
            for move_line in stock_pick_lines:
                for move in move_line.move_lines:
                    if move.product_id.id == catgory_product:
                        internal_cat = move.product_uom_qty
            available_qty = product.virtual_available + \
                            product.outgoing_qty - \
                            product.incoming_qty
            value = available_qty * product.standard_price
            vals = {
                'category': product.categ_id.name,
                'cost_price': product.standard_price or 0,
                'available': available_qty or 0,
                'virtual': product.virtual_available or 0,
                'incoming': product.incoming_qty or 0,
                'outgoing': product.outgoing_qty or 0,
                'net_on_hand': product.qty_available or 0,
                'total_value': value,
                'sale_value': sale_value or 0,
                'purchase_value': purchase_value or 0,
                'beginning':beginning or 0,
                'internal':internal_cat or 0,
            }
            lines.append(vals)
        return lines

    @api.multi  
    def print_exl_report(self):
        filename = 'Stock Valuation Report.xls'
        get_warehouse = self.get_warehouse()
        get_warehouse_name = self._get_warehouse_name()
        l1 = []
        get_company = self.get_company()
        get_currency = self.get_currency()
        workbook = xlwt.Workbook()
        stylePC = xlwt.XFStyle()
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        fontP = xlwt.Font()
        fontP.bold = True
        fontP.height = 200
        stylePC.font = fontP
        stylePC.num_format_str = '@'
        stylePC.alignment = alignment
        style_title = xlwt.easyxf("font:height 300; font: name Liberation Sans, bold on,color black; align: horiz center")
        style_table_header = xlwt.easyxf("font:height 200; font: name Liberation Sans, bold on,color black; align: horiz center")
        style = xlwt.easyxf("font:height 200; font: name Liberation Sans,color black;")
        worksheet = workbook.add_sheet('Sheet 1')
        worksheet.write(3, 1, 'Start Date:', style_table_header)
        worksheet.write(4, 1, self.start_date)
        worksheet.write(3, 3, 'End Date', style_table_header)
        worksheet.write(4, 3, self.end_date)
        worksheet.write(3, 4, 'Company', style_table_header)
        worksheet.write(4, 4, get_company and get_company[0] or '',)
        worksheet.write(3, 6, 'Warehouse(s)', style_table_header)
        worksheet.write(3, 5, 'Currency', style_table_header)
        worksheet.write(4, 5, get_currency and get_currency[0] or '',)
        w_col_no = 7
        w_col_no1 = 8
        if get_warehouse_name:
               # w_col_no = w_col_no + 8
            worksheet.write(4, 6,get_warehouse_name, stylePC)
               # w_col_no1 = w_col_no1 + 9
        if self.display_sum:
            worksheet.write_merge(0, 0, 0, 5, "Inventory Valuation Summary Report", style=style_title)
            worksheet.write(6, 0, 'Category', style_table_header)
            worksheet.write(6, 1, 'Cost Price', style_table_header)
            worksheet.write(6, 2, 'Beginning', style_table_header)
            worksheet.write(6, 3, 'Internal', style_table_header)
            worksheet.write(6, 4, 'Received', style_table_header)
            worksheet.write(6, 5, 'Sales', style_table_header)
            worksheet.write(6, 6, 'Adjustment', style_table_header)
            worksheet.write(6, 7, 'Ending', style_table_header)
            worksheet.write(6, 8, 'Valuation', style_table_header)
            prod_row = 7
            prod_col = 0
            for i in get_warehouse:
                get_line = self.get_data()
                for each in get_line:
                    worksheet.write(prod_row, prod_col, each['category'], style)
                    worksheet.write(prod_row, prod_col+1, each['cost_price'], style)
                    worksheet.write(prod_row, prod_col+2, each['beginning'], style)
                    worksheet.write(prod_row, prod_col+3, each['internal'], style)
                    worksheet.write(prod_row, prod_col+4, each['incoming'], style)
                    worksheet.write(prod_row, prod_col+5, each['sale_value'], style)
                    worksheet.write(prod_row, prod_col+6, each['outgoing'], style)
                    worksheet.write(prod_row, prod_col+7, each['net_on_hand'], style)
                    worksheet.write(prod_row, prod_col+8, each['total_value'], style)
                    prod_row = prod_row + 1
                break
            prod_row = 6
            prod_col = 7
        else:
            worksheet.write_merge(0, 0, 0, 5, "Inventory Valuation Report", style=style_title)
            worksheet.write(6, 0, 'Default Code', style_table_header)
            worksheet.write(6, 1, 'Name', style_table_header)
            worksheet.write(6, 2, 'Category', style_table_header)
            worksheet.write(6, 3, 'Cost Price', style_table_header)
            worksheet.write(6, 4, 'Beginning', style_table_header)
            worksheet.write(6, 5, 'Internal', style_table_header)
            worksheet.write(6, 6, 'Received', style_table_header)
            worksheet.write(6, 7, 'Sales', style_table_header)
            worksheet.write(6, 8, 'Adjustment', style_table_header)
            worksheet.write(6, 9, 'Ending', style_table_header)
            worksheet.write(6, 10, 'Valuation', style_table_header)
            prod_row = 7
            prod_col = 0
            for i in get_warehouse:
                get_line = self.get_lines(i)
                for each in get_line:
                    worksheet.write(prod_row, prod_col, each['sku'], style)
                    worksheet.write(prod_row, prod_col+1, each['name'], style)
                    worksheet.write(prod_row, prod_col+2, each['category'], style)
                    worksheet.write(prod_row, prod_col+3, each['cost_price'], style)
                    worksheet.write(prod_row, prod_col+4, each['beginning'], style)
                    worksheet.write(prod_row, prod_col+5, each['internal'], style)
                    worksheet.write(prod_row, prod_col+6, each['incoming'], style)
                    worksheet.write(prod_row, prod_col+7, each['sale_value'], style)
                    worksheet.write(prod_row, prod_col+8, each['outgoing'], style)
                    worksheet.write(prod_row, prod_col+9, each['net_on_hand'], style)
                    worksheet.write(prod_row, prod_col+10, each['total_value'], style)
                    prod_row = prod_row + 1
                break
            prod_row = 6
            prod_col = 7
        fp = StringIO()
        workbook.save(fp)
        
        export_id = self.env['sale.day.book.report.excel'].create({'excel_file': base64.encodestring(fp.getvalue()), 'file_name': filename})
        res = {
                        'view_mode': 'form',
                        'res_id': export_id.id,
                        'res_model': 'sale.day.book.report.excel',
                        'view_type': 'form',
                        'type': 'ir.actions.act_window',
                        'target':'new'
                }
        return res
        


class sale_day_book_report_excel(models.TransientModel):
    _name = "sale.day.book.report.excel"
    
    
    excel_file = fields.Binary('Excel Report For Inventory Valuation ')
    file_name = fields.Char('Excel File', size=64)



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
