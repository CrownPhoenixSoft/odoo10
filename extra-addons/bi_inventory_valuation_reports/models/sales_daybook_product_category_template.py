# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.


from odoo import models, api


class sales_daybook_product_category_report(models.AbstractModel):
    _name = 'report.bi_inventory_valuation_reports.sales_daybook_template'

    @api.model
    def render_html(self, docids, data=None):
        data = data if data is not None else {}
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('bi_inventory_valuation_reports.sales_daybook_template')
        docargs = {
                   'doc_ids': self.ids,
                   'doc_model': report.model,
                   'docs': self.ids,
                   'data' : data,
                   'get_warehouse' : self._get_warehouse_name,
                   'get_company':self._get_company,
                   'get_currency':self._get_currency,
                   'get_lines':self._get_lines,
                   'get_data' : self._get_data,
                   }
        return report_obj.render('bi_inventory_valuation_reports.sales_daybook_template', docargs)

    def _get_warehouse_name(self,data):
        if data['warehouse']:
            l1 = []
            l2 = []
            for i in data['warehouse']:
                obj = self.env['stock.warehouse'].search([('id', 'in', data['warehouse'])])
                for j in obj:
                    l1.append(j.name)
                    myString = ",".join(l1 )
                return myString
        return ''
    
    def _get_company(self, data):
        if data['company_id']:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('name', '=', data['company_id'])])
            l1.append(obj.name)
            return l1
        return ''

    def _get_currency(self,data):
        if data['company_id']:
            l1 = []
            l2 = []
            obj = self.env['res.company'].search([('name', '=', data['company_id'])])
            l1.append(obj.currency_id.name)
            return l1
        return ''
    
    def _get_lines(self, data):
        cat_list = []
        category_obj = self.env['product.category']
        lines = []
        loc_list = []
        type_list = []
        beginning = 0
        if data['warehouse']:
            l1 = []
            l2 = []
            for i in data['warehouse']:
                obj = self.env['stock.warehouse'].search([('id', 'in', data['warehouse'])])
                for j in obj:
                    l1.append(j.id)
        stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date'])])
        if data['company_id']:
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('company_id', '=', data['company_id'])])
        if data['category']:
            for cat in data['category']:
                cat_list.append(cat)
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('product_categ_id', 'in', cat_list)])
        if data['category'] and data['company_id']:
            for cat in data['category']:
                cat_list.append(cat.id)
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('product_categ_id', 'in', cat_list),('company_id', '=', data['company_id'])])
        stock_list = []
        product_list = []
        for i in stock_history:
            if i.product_id.id not in product_list:
                product_list.append(i.product_id.id)
        for pro in product_list:
            sale_value = 0
            purchase_value = 0
            internal = 0
            internal_cat = 0
            product = self.env['product.product'].browse(pro)
            sale_obj = self.env['sale.order.line'].search([('order_id.state', 'in', ('sale', 'done')),
                                                           ('product_id', '=', product.id),
                                                           ('order_id.warehouse_id', 'in', l1)])
            for i in sale_obj:
                sale_value = sale_value + i.product_uom_qty
            purchase_obj = self.env['purchase.order.line'].search([('order_id.state', 'in', ('purchase', 'done')),
                                                                   ('product_id', '=', product.id),
                                                                   ('order_id.picking_type_id', 'in', l1)])
            for i in purchase_obj:
                purchase_value = purchase_value + i.product_qty
            stock_inv_line_obj = self.env['stock.inventory.line']
            stock_loc_obj = self.env['stock.location'].search([('usage','=','internal')])
            for j in stock_loc_obj:
                loc_list.append(j.id)
            stock_inv_lines = stock_inv_line_obj.search([('product_id', '=', pro),('location_id', 'in', loc_list)])
            for b in stock_inv_lines:
                beginning = b.product_qty
            stock_pick_type_obj = self.env['stock.picking.type'].search([('code','=','internal')])
            for k in stock_pick_type_obj:
                type_list.append(k.id)
            stock_pick_obj = self.env['stock.picking']
            stock_pick_lines = stock_pick_obj.search([('picking_type_id', 'in', type_list)])
            for move_line in stock_pick_lines:
                for move in move_line:
                    if move.product_id == product.id:
                        internal = move.product_uom_qty
            available_qty = product.with_context({'warehouse': data['warehouse']}).virtual_available + \
                            product.with_context({'warehouse': data['warehouse']}).outgoing_qty - \
                            product.with_context({'warehouse': data['warehouse']}).incoming_qty
            value = available_qty * product.standard_price
            vals = {
                'sku': product.default_code,
                'name': product.name,
                'category': product.categ_id.name,
                'cost_price': product.standard_price,
                'available': available_qty,
                'virtual': product.with_context({'warehouse': data['warehouse']}).virtual_available,
                'incoming': product.with_context({'warehouse': data['warehouse']}).incoming_qty,
                'outgoing': product.with_context({'warehouse': data['warehouse']}).outgoing_qty,
                'net_on_hand': product.with_context({'warehouse': data['warehouse']}).qty_available,
                'total_value': value,
                'sale_value': sale_value,
                'purchase_value': purchase_value,
                'beginning':beginning,
                'internal':internal,
            }
            lines.append(vals)
        return lines


    def _get_data(self,data):
        vals = {}
        lines = []
        cat_list=[]
        category_obj = self.env['product.category']
        category_ids = category_obj.search([])
        lines = []
        loc_list = []
        type_list = []
        c_list=[]
        t_list=[]
        sale_value = 0
        purchase_value = 0
        internal = 0
        internal_cat = 0
        beginning = 0
        available_qty = 0
        value = 0
        virtual_avail = 0
        income = 0
        out = 0
        qty_avail = 0
        if data['warehouse']:
            l1 = []
            l2 = []
            for i in data['warehouse']:
                obj = self.env['stock.warehouse'].search([('id', 'in', data['warehouse'])])
                for j in obj:
                    l1.append(j.id)
        for c in category_ids:
            cat_list.append(c.id)
        stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('product_categ_id', 'in', cat_list)])
        if data['company_id']:
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('company_id', '=', data['company_id'])])
        if data['category']:
            for cat in data['category']:
                cat_list.append(cat)
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('product_categ_id', 'in', cat_list)])
        if data['category'] and data['company_id']:
            for cat in data['category']:
                cat_list.append(cat)
            stock_history = self.env['stock.history'].search([('date', '>=', data['start_date']),('date', '<=', data['end_date']),('product_categ_id', 'in', cat_list),('company_id', '=', data['company_id'])])
        stock_list = []
        product_list = []
        for i in stock_history:
            if i.product_id.id not in product_list:
                product_list.append(i.product_id.id)
                c_list.append(i.product_id.categ_id.name)
        for i in c_list:
            if i not in t_list:
                t_list.append(i)
        sale_value = 0
        purchase_value = 0
        internal = 0
        internal_cat = 0
        beginning = 0
        available_qty = 0
        value = 0
        virtual_avail = 0
        income = 0
        out = 0
        qty_avail = 0
        for cat in t_list:
            for catgory_product in product_list:
                product = self.env['product.product'].browse(catgory_product)
                if cat == product.categ_id.id:
                    sale_obj = self.env['sale.order.line'].search([('order_id.state', 'in', ('sale', 'done')),
                                                           ('product_id', '=', catgory_product),
                                                           ('order_id.warehouse_id', 'in', l1)])
                    if sale_obj:
                        for i in sale_obj:
                            sale_value += sale_value + i.product_uom_qty
                    purchase_obj = self.env['purchase.order.line'].search([('order_id.state', 'in', ('purchase', 'done')),
                                                                   ('product_id', '=', catgory_product),
                                                                   ('order_id.picking_type_id', 'in', l1)])
                    if purchase_obj:
                        for i in purchase_obj:
                            purchase_value += purchase_value + i.product_qty
                    stock_inv_line_obj = self.env['stock.inventory.line']
                    stock_loc_obj = self.env['stock.location'].search([('usage','=','internal')])
                    for j in stock_loc_obj:
                        loc_list.append(j.id)
                    stock_inv_lines = stock_inv_line_obj.search([('product_id', '=', catgory_product),('location_id', 'in', loc_list)])
                    for b in stock_inv_lines:
                        beginning += b.product_qty
                    stock_pick_type_obj = self.env['stock.picking.type'].search([('code','=','internal')])
                    for k in stock_pick_type_obj:
                        type_list.append(k.id)
                    stock_pick_obj = self.env['stock.picking']
                    stock_pick_lines = stock_pick_obj.search([('picking_type_id', 'in', type_list)])
                    for move_line in stock_pick_lines:
                        for move in move_line.move_lines:
                            if move.product_id.id == catgory_product:
                                internal_cat += move.product_uom_qty
                available_qty += product.virtual_available + \
                                product.outgoing_qty - \
                                product.incoming_qty
                value += available_qty * product.standard_price
                virtual_avail += product.virtual_available
                income += product.incoming_qty
                out += product.outgoing_qty
                qty_avail += product.qty_available
            vals= {
                'category': cat,
                'available': available_qty or 0,
                'virtual': virtual_avail or 0,
                'incoming': income or 0,
                'outgoing': out or 0,
                'net_on_hand': qty_avail or 0,
                'total_value': value,
                'sale_value': sale_value or 0,
                'purchase_value': purchase_value or 0,
                'beginning':beginning,
                'internal':internal_cat or 0,
            }
            lines.append(vals)
        return lines
            

        



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
