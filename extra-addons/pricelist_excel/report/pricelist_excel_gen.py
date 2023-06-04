# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 GRIMMETTE,LLC <info@grimmette.com>

import base64
import copy
import datetime
from itertools import chain
import logging
import os
import re
import shutil
import tempfile
from zipfile import ZipFile, ZIP_DEFLATED, BadZipfile
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessError
from odoo.tools.mimetypes import guess_mimetype
from odoo.tools.safe_eval import safe_eval
from odoo.tools import float_round
from ..models.xlsx import XLSXEdit
_logger = logging.getLogger(__name__)
SUPPORTED_FORMATS = ('.xlsx', '.xlsm')
class PricelistExcelGen(models.TransientModel):
    _name = 'pricelist_excel_gen'
    def _validate_archive(self, file, filename):
        is_file_like = hasattr(filename, 'read')
        if not is_file_like and os.path.isfile(filename):
            file_format = os.path.splitext(filename)[-1].lower()
            if file_format not in SUPPORTED_FORMATS:
                if file_format == '.xls':
                    msg = ('Does not support the old .xls file format, '
                           'please convert it to .xlsx or .xlsm file format.')
                elif file_format == '.xlsb':
                    msg = ('Does not support binary format .xlsb, '
                           'please convert this file to .xlsx or .xlsm format.')
                else:
                    msg = ('Does not support %s file format, '
                           'please check you can open '
                           'it with Excel first. '
                           'Supported formats are: %s') % (file_format,
                                                           ','.join(SUPPORTED_FORMATS))
                raise UserError(msg)
        if is_file_like:
            if getattr(file, 'encoding', None) is not None:
                raise IOError("File-object must be opened in binary mode")
        try:
            archive = ZipFile(file, 'r', ZIP_DEFLATED)
            archive.testzip()
            archive.close() 
            arc_check = True
        except BadZipfile:
            msg = ('Does not support the file format, '
                   'please use .xlsx file format.')
            arc_check = False
        return arc_check
    @api.model
    @api.returns('ir.attachment', lambda value: value.id)
    def _get_template(self, template_id):
        return self.env['ir.attachment'].search([('res_model', '=', 'product.pricelist_excel'), ('id', '=', template_id)])
    def _get_conf(self, conf_id):
        return self.env['product.pricelist_excel'].search([('id', '=', conf_id)])
    def copyFile(self,src, dest):
        try:
            shutil.copy(src, dest)
        except shutil.Error as e:
            _logger.info('Error: %s' % e)
        except IOError as e:
            _logger.info('Error: %s' % e.strerror)
    @api.multi
    def create_xls(self, datas=None, use_new_cursor=False):
        datas = datas if datas is not None else {}
        if use_new_cursor:
            cr = registry(self._cr.dbname).cursor()
            self = self.with_env(self.env(cr=cr))
        tmp_dir = tempfile.gettempdir()
        res_conf = self._get_conf(datas['form']['pricelist_conf_id']) or {}
        active_ids = datas['ids']
        out_file_name = datetime.datetime.now().strftime(res_conf['out_file_name'])
        template_xlsx = 0    
        if res_conf:
            template_xlsx = res_conf['template_name_id']
        tmpfile_wfd, tmpfile_wpath = tempfile.mkstemp(suffix='.xlsx', prefix='xslx.tmpl.tmp.')
        if template_xlsx:
            template = {} 
            template = self._get_template(template_xlsx.id)
            fname = template['datas_fname']
            store_fname = template['store_fname']
            template_fp = template._full_path(store_fname)
            self.copyFile(template_fp,tmpfile_wpath)
        else:
            base_template_fp = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'pricelist_template.xlsx')
            self.copyFile(base_template_fp,tmpfile_wpath)
        if res_conf:
            pricelist_id = res_conf.pricelist_id.id
        pricelist = self.env['product.pricelist'].browse(pricelist_id)  
        products = self.env['product.product'].browse(datas.get('ids', datas.get('active_ids')))
        quantities = self._get_quantity(datas)
        categories_data = self._get_categories(pricelist, products, quantities)
        categories = self.env['product.category'].search([])
        cat_conf = {} 
        for category in categories:
            cat_conf[category.id] = [category.display_name, category.name, category.parent_id.id, category.child_id.ids, category.category_code, 0, False]
        for cd in categories_data:
            cat_conf[cd['category'].id][6] = True
            b = cat_conf[cd['category'].id][6]
            cid = cd['category'].id
            while b:
                if cat_conf[cid][2]:
                    cat_conf[cid][6] = True
                    cat_level = (cat_conf[cid][0]).split("/")
                    cat_conf[cid][5] = len(cat_level)-1
                    cid = cat_conf[cid][2]
                else:
                    cat_conf[cid][6] = True
                    cat_level = (cat_conf[cid][0]).split("/")
                    cat_conf[cid][5] = len(cat_level)-1
                    b = False
        res_cat_sort = [[key,value] for key, value in sorted(cat_conf.iteritems(), key=lambda (k,v): (v,k))]            
        currency_name = pricelist.currency_id.display_name  
        user = self.env['res.users'].browse(self.env.uid)
        company_name=user.company_id.display_name
        xlsx_template = XLSXEdit(tmpfile_wpath)
        _str_finder = re.compile('(\D+)')
        _num_finder = re.compile('(\d+)')
        qtys = res_conf.qty_reference
        qty1,qty5 = qtys.split(":")
        qty1_letter, row_data  = xlsx_template.coordinate_from_string(qty1)
        qty1_index = xlsx_template.column_index_from_string(qty1_letter)
        qty2_letter = xlsx_template.get_column_letter(qty1_index+1)
        qty3_letter = xlsx_template.get_column_letter(qty1_index+2)
        qty4_letter = xlsx_template.get_column_letter(qty1_index+3)
        qty5_letter = xlsx_template.get_column_letter(qty1_index+4)
        conf_data = {'header_conf':{},'header_filter':{},'header_data':{},'filter':{},'data':{}}
        if template_xlsx:
            conf_data['header_conf']['sheet_reference'] =  res_conf.sheet_reference
            conf_data['header_conf']['header_reference'] =  res_conf.header_reference
            conf_data['header_conf']['qty_reference'] =  res_conf.qty_reference
            conf_data['header_filter']['company_bool'] =  res_conf.company_bool
            conf_data['header_filter']['price_name_bool'] =  res_conf.price_name_bool
            conf_data['header_filter']['currency_bool'] =  res_conf.currency_bool
            conf_data['header_filter']['print_date_bool'] =  res_conf.print_date_bool
            conf_data['header_data']['company_reference'] =  res_conf.company_reference
            conf_data['header_data']['price_name_reference'] =  res_conf.price_name_reference
            conf_data['header_data']['currency_reference'] =  res_conf.currency_reference
            conf_data['header_data']['print_date_reference'] =  res_conf.print_date_reference
            conf_data['filter']['show_categories'] =  res_conf.show_categories
            conf_data['filter']['category_style'] =  res_conf.category_style
            conf_data['filter']['show_categories_code'] =  res_conf.show_categories_code
            conf_data['filter']['show_level'] =  res_conf.show_level
            conf_data['filter']['show_autofilter'] =  res_conf.show_autofilter
            conf_data['filter']['show_images'] =  res_conf.show_images
            conf_data['filter']['wraptxt'] =  res_conf.wraptxt
            conf_data['data']['product_code'] = [res_conf.product_code_cell_reference, res_conf.product_code_bool]
            conf_data['data']['product_name'] = [res_conf.product_name_cell_reference, res_conf.product_name_bool]
            conf_data['data']['attributes'] = [res_conf.attributes_cell_reference, res_conf.attributes_bool]
            conf_data['data']['qty1'] = [qty1, bool(datas.get('form',{}).get('qty1'))]
            conf_data['data']['qty2'] = [qty2_letter+str(row_data), bool(datas.get('form',{}).get('qty2'))]
            conf_data['data']['qty3'] = [qty3_letter+str(row_data), bool(datas.get('form',{}).get('qty3'))]
            conf_data['data']['qty4'] = [qty4_letter+str(row_data), bool(datas.get('form',{}).get('qty4'))]
            conf_data['data']['qty5'] = [qty5_letter+str(row_data), bool(datas.get('form',{}).get('qty5'))]
            conf_data['data']['vat'] = [res_conf.vat_cell_reference, res_conf.vat_bool]
            conf_data['data']['uom'] = [res_conf.uom_cell_reference, res_conf.uom_bool]
            conf_data['data']['qty_case'] = [res_conf.qty_case_cell_reference, res_conf.qty_case_bool]
            conf_data['data']['onhand'] = [res_conf.onhand_cell_reference, res_conf.onhand_bool]
            conf_data['data']['hscode'] = [res_conf.hscode_cell_reference, res_conf.hscode_bool]
            conf_data['data']['ean'] = [res_conf.ean_cell_reference, res_conf.ean_bool]
            conf_data['data']['weight'] = [res_conf.weight_cell_reference, res_conf.weight_bool]
            conf_data['data']['volume'] = [res_conf.volume_cell_reference, res_conf.volume_bool]
            conf_data['data']['description'] = [res_conf.description_cell_reference, res_conf.description_bool]
            conf_data['data']['customer_lead_time'] = [res_conf.customer_lead_time_cell_reference, res_conf.customer_lead_time_bool]
        else:
            conf_data['header_conf']['sheet_reference'] =  'Sheet1'
            conf_data['header_conf']['header_reference'] =  'A6:R6'
            conf_data['header_conf']['qty_reference'] =  'D7:H7'
            conf_data['header_filter']['company_bool'] =  True
            conf_data['header_filter']['price_name_bool'] =  True
            conf_data['header_filter']['currency_bool'] =  True
            conf_data['header_filter']['print_date_bool'] =  True
            conf_data['header_data']['company_reference'] =  'A1'
            conf_data['header_data']['price_name_reference'] =  'A3'
            conf_data['header_data']['currency_reference'] =  'A4'
            conf_data['header_data']['print_date_reference'] =  'A5'
            conf_data['filter']['show_categories'] =  res_conf.show_categories
            conf_data['filter']['category_style'] =  res_conf.category_style
            conf_data['filter']['show_categories_code'] =  res_conf.show_categories_code
            conf_data['filter']['show_level'] =  res_conf.show_level
            conf_data['filter']['show_autofilter'] =  res_conf.show_autofilter
            conf_data['filter']['show_images'] =  res_conf.show_images
            conf_data['filter']['wraptxt'] =  res_conf.wraptxt
            conf_data['data']['product_code'] = ['A7', res_conf.product_code_bool]
            conf_data['data']['product_name'] = ['B7', res_conf.product_name_bool]
            conf_data['data']['attributes'] = ['C7', res_conf.attributes_bool]
            conf_data['data']['qty1'] = ['D7', bool(datas.get('form',{}).get('qty1'))]
            conf_data['data']['qty2'] = ['E7', bool(datas.get('form',{}).get('qty2'))]
            conf_data['data']['qty3'] = ['F7', bool(datas.get('form',{}).get('qty3'))]
            conf_data['data']['qty4'] = ['G7', bool(datas.get('form',{}).get('qty4'))]
            conf_data['data']['qty5'] = ['H7', bool(datas.get('form',{}).get('qty5'))]
            conf_data['data']['vat'] = ['I7', res_conf.vat_bool]
            conf_data['data']['uom'] = ['J7', res_conf.uom_bool]
            conf_data['data']['qty_case'] = ['K7', res_conf.qty_case_bool]
            conf_data['data']['onhand'] = ['L7', res_conf.onhand_bool]
            conf_data['data']['hscode'] = ['M7', res_conf.hscode_bool]
            conf_data['data']['ean'] = ['N7', res_conf.ean_bool]
            conf_data['data']['weight'] = ['O7', res_conf.weight_bool]
            conf_data['data']['volume'] = ['P7', res_conf.volume_bool]
            conf_data['data']['description'] = ['Q7', res_conf.description_bool]
            conf_data['data']['customer_lead_time'] = ['R7', res_conf.customer_lead_time_bool]
        conf_data_out = copy.deepcopy(conf_data)            
        xlsx_template.write_conf(conf_data_out)
        res_header_data = [[key,value] for key, value in sorted(conf_data['header_data'].iteritems(), key=lambda (k,v): (v,k))]
        res_header_data_ind = [] 
        for n in res_header_data:
            letter, row  = xlsx_template.coordinate_from_string(n[1])
            letter_index = xlsx_template.column_index_from_string(letter)
            res_header_data_ind.append([n[0], letter_index, row])
        res_header_data_ind_out = copy.deepcopy(res_header_data_ind)
        res_data = [[key,value] for key, value in sorted(conf_data['data'].iteritems(), key=lambda (k,v): (v,k))]
        res_data_ind = [] 
        for n in res_data:
            letter, row  = xlsx_template.coordinate_from_string(n[1][0])
            letter_index = xlsx_template.column_index_from_string(letter)
            res_data_ind.append([n[0], letter_index, row, n[1][1]])
        res_data_ind_out = copy.deepcopy(res_data_ind)
        for i in res_data_ind_out:
            if i[3] == False:
                for ih in res_header_data_ind_out:
                    if ih[1] >= i[1]:
                        ih[1] = ih[1]-1
                for io in res_data_ind_out:
                    if io[1] > i[1]:
                        io[1] = io[1]-1
        for i in res_header_data_ind_out:
            conf_data_out['header_data'][i[0]] = xlsx_template.cell_from_index(i[1],i[2]) 
        for i in res_data_ind_out:
            conf_data_out['data'][i[0]] = xlsx_template.get_column_letter(i[1]) 
        xlsx_template.update_conf(conf_data_out)
        header_1, header_2 = conf_data['header_conf']['header_reference'].split(":")
        header_row_index = _num_finder.findall(header_1)[0]
        sheet_ref = conf_data['header_conf']['sheet_reference']
        start_row_index = header_row_index 
        for n in res_data_ind:
            if n[3] == False:
                letter  = xlsx_template.get_column_letter(n[1])
                xlsx_template.remove_culumn(sheet_ref, letter)     
        xlsx_template.shift_coordinate(sheet_ref, res_data_ind_out)
        xlsx_template.add_format(conf_data_out['data']['product_name'], conf_data['filter']['category_style'])
        col_false = []
        for key, values in conf_data['data'].iteritems():
            if not values[1]:
                col, row = xlsx_template.coordinate_from_string(values[0])
                col_false.append(col)
        if conf_data['header_filter']['company_bool']:
            col, row = xlsx_template.coordinate_from_string(conf_data['header_data']['company_reference']) 
            if col not in col_false: 
                xlsx_template.write(sheet_ref, conf_data_out['header_data']['company_reference'], company_name)
        if conf_data['header_filter']['price_name_bool']:        
            col, row = xlsx_template.coordinate_from_string(conf_data['header_data']['price_name_reference']) 
            if col not in col_false: 
                xlsx_template.write(sheet_ref, conf_data_out['header_data']['price_name_reference'], res_conf.name)
        if conf_data['header_filter']['currency_bool']:
            col, row = xlsx_template.coordinate_from_string(conf_data['header_data']['currency_reference']) 
            if col not in col_false: 
                    xlsx_template.write(sheet_ref, conf_data_out['header_data']['currency_reference'], currency_name)
        if conf_data['header_filter']['print_date_bool']:
            col, row = xlsx_template.coordinate_from_string(conf_data['header_data']['print_date_reference']) 
            if col not in col_false: 
                xlsx_template.write(sheet_ref, conf_data_out['header_data']['print_date_reference'], datetime.datetime.now())
        if not template_xlsx:
            if conf_data['data']['qty1'][1]:
                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty1'], header_row_index), ''.join([str(datas.get('form',{}).get('qty1')),' ', 'units']))
            if conf_data['data']['qty2'][1]:
                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty2'], header_row_index), ''.join([str(datas.get('form',{}).get('qty2')),' ', 'units']))
            if conf_data['data']['qty3'][1]:
                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty3'], header_row_index), ''.join([str(datas.get('form',{}).get('qty3')),' ', 'units']))
            if conf_data['data']['qty4'][1]:
                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty4'], header_row_index), ''.join([str(datas.get('form',{}).get('qty4')),' ', 'units']))
            if conf_data['data']['qty5'][1]:
                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty5'], header_row_index), ''.join([str(datas.get('form',{}).get('qty5')),' ', 'units']))
        ncell,nrow = xlsx_template.coordinate_from_string(conf_data['data']['qty1'][0]) 
        for i in res_cat_sort:
            if i[1][6]:
                if conf_data['filter']['show_categories']:
                    cell_cat = xlsx_template.cell_from_coordinate(conf_data_out['data']['product_name'],nrow)
                    xlsx_template.write(sheet_ref, cell_cat, i[1][1], i[1][5], True)
                    nrow += 1
                for cd in categories_data:
                    if cd['category'].id == i[0]:
                        for idp in cd['products'].ids:
                            if conf_data['data']['product_code'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['product_code'],nrow), cd['prices'][idp]['default_code'], i[1][5]+1)
                            if conf_data['data']['product_name'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['product_name'],nrow), cd['prices'][idp]['name'], i[1][5]+1)
                            if conf_data['data']['attributes'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['attributes'],nrow), cd['prices'][idp]['attributes'], i[1][5]+1)
                            if conf_data['data']['qty1'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty1'],nrow), cd['prices'][idp][datas.get('form',{}).get('qty1')], i[1][5]+1)
                            if conf_data['data']['qty2'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty2'],nrow), cd['prices'][idp][datas.get('form',{}).get('qty2')], i[1][5]+1)
                            if conf_data['data']['qty3'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty3'],nrow), cd['prices'][idp][datas.get('form',{}).get('qty3')], i[1][5]+1)
                            if conf_data['data']['qty4'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty4'],nrow), cd['prices'][idp][datas.get('form',{}).get('qty4')], i[1][5]+1)
                            if conf_data['data']['qty5'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty5'],nrow), cd['prices'][idp][datas.get('form',{}).get('qty5')], i[1][5]+1)
                            if conf_data['data']['vat'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['vat'],nrow), cd['prices'][idp]['tax'], i[1][5]+1)
                            if conf_data['data']['uom'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['uom'],nrow), cd['prices'][idp]['uom'], i[1][5]+1)
                            if conf_data['data']['qty_case'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['qty_case'],nrow), cd['prices'][idp]['packaging'], i[1][5]+1)
                            if conf_data['data']['onhand'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['onhand'],nrow), cd['prices'][idp]['virtual_available'], i[1][5]+1)
                            if conf_data['data']['hscode'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['hscode'],nrow), cd['prices'][idp]['hs_code'], i[1][5]+1)
                            if conf_data['data']['ean'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['ean'],nrow), cd['prices'][idp]['barcode'], i[1][5]+1)
                            if conf_data['data']['weight'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['weight'],nrow), cd['prices'][idp]['weight'], i[1][5]+1)
                            if conf_data['data']['volume'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['volume'],nrow), cd['prices'][idp]['volume'], i[1][5]+1)
                            if conf_data['data']['description'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['description'],nrow), cd['prices'][idp]['description_sale'], i[1][5]+1)
                            if conf_data['data']['customer_lead_time'][1]:
                                xlsx_template.write(sheet_ref, xlsx_template.cell_from_coordinate(conf_data_out['data']['customer_lead_time'],nrow), cd['prices'][idp]['sale_delay'], i[1][5]+1)
                            nrow += 1
        out_tmpfile_wpath = ''.join([xlsx_template._zip_folder, '.xlsx'])
        with open(out_tmpfile_wpath, 'w') as zip_file:
            zip_file.write(xlsx_template.get_content())
        zipOb = ZipFile(out_tmpfile_wpath)
        zipOb.testzip()
        zipOb.close() 
        with open(out_tmpfile_wpath,'rb') as m:
            data_attach = {
                'name': res_conf.name,
                'datas': base64.b64encode(m.read()),
                'type': "binary",
                'datas_fname': out_file_name,
                'res_model': res_conf._name,
                'res_id': 0,
                'res_id_ext': res_conf.id,
            }
            try:
                new_attach = self.env['ir.attachment'].create(data_attach)
            except AccessError:
                _logger.info("Cannot save %r as attachment", out_file_name)
            else:
                _logger.info('The document %s is now saved in the database', out_file_name)
        new_attach_fpath = ''
        new_attach_fname = ''
        if new_attach: 
            new_attach_fname = new_attach['datas_fname']
            store_fname = new_attach['store_fname']
            new_attach_fpath = new_attach._full_path(store_fname)
        self._validate_archive(new_attach_fpath, new_attach_fname)
        file_obj = {
            'type': 'ir.actions.act_url',
            'url': '/pricelist_excel?id=%s&filename=%s' % (new_attach.id, new_attach_fname,),
            'target': 'self',
        }
        return file_obj
    def _get_quantity(self, data):
        return sorted([data['form'][key] for key in data['form'].keys() if key.startswith('qty') and data['form'][key]])
    def _get_categories(self, pricelist, products, quantities):
        categ_data = []
        categories = self.env['product.category']
        for product in products:
            categories |= product.categ_id
        for category in categories:
            categ_products = products.filtered(lambda product: product.categ_id == category)
            prices = {}
            for categ_product in categ_products:
                prices[categ_product.id] = dict.fromkeys(quantities, 0.0)
                for quantity in quantities:
                    prices[categ_product.id][quantity] = self._get_price(pricelist, categ_product, quantity)
                if categ_product.default_code:
                    prices[categ_product.id]['default_code'] = categ_product.default_code
                else:
                    prices[categ_product.id]['default_code'] = ''
                prices[categ_product.id]['name'] = categ_product.name
                if self._get_attributes(categ_product):
                    prices[categ_product.id]['attributes'] = self._get_attributes(categ_product)
                else:
                    prices[categ_product.id]['attributes'] = ''
                if categ_product.description_sale:
                    prices[categ_product.id]['description_sale'] = categ_product.description_sale
                else:
                    prices[categ_product.id]['description_sale'] = ''
                prices[categ_product.id]['qty_available'] = categ_product.qty_available
                prices[categ_product.id]['virtual_available'] = categ_product.virtual_available
                prices[categ_product.id]['uom'] = categ_product.uom_id.name
                prices[categ_product.id]['weight'] = categ_product.weight
                prices[categ_product.id]['volume'] = categ_product.volume
                prices[categ_product.id]['sale_delay'] = categ_product.sale_delay
                if categ_product.barcode:
                    prices[categ_product.id]['barcode'] = categ_product.barcode
                else:
                    prices[categ_product.id]['barcode'] = ''
                if categ_product.hs_code:  
                    prices[categ_product.id]['hs_code'] = categ_product.hs_code
                else:
                    prices[categ_product.id]['hs_code'] = ''
                if self._get_taxes(categ_product):
                    prices[categ_product.id]['tax'] = self._get_taxes(categ_product)     
                else:
                    prices[categ_product.id]['tax'] = ''
                if self._get_packaging(categ_product):
                    prices[categ_product.id]['packaging'] = self._get_packaging(categ_product)    
                else:
                    prices[categ_product.id]['packaging'] = ''
            categ_data.append({
                'category': category,
                'products': categ_products,
                'prices': prices,
            })
        return categ_data
    def _get_price(self, pricelist, product, qty):
        sale_price_digits = self.env['decimal.precision'].precision_get('Product Price')
        price = pricelist.get_product_price(product, qty, False)
        if not price:
            price = product.list_price
        return float_round(price, precision_digits=sale_price_digits)
    def _get_attributes(self, product):
        attrs = self.env['product.attribute.value'].browse(product.attribute_value_ids.ids)
        attrs_str = ''
        i = 1
        for p in attrs:
            attrs_str += p.display_name    
            if len(attrs) != i:
                attrs_str += ', ' 
            i += 1 
        return attrs_str
    def _get_taxes(self, product):
        taxes = self.env['account.tax'].browse(product.taxes_id.ids)
        taxes_str = ''
        i = 1
        for p in taxes:
            taxes_str += p.display_name    
            if len(taxes) != i:
                taxes_str += ', ' 
            i += 1 
        return taxes_str
    def _get_packaging(self, product):
        packaging = self.env['product.packaging'].browse(product.packaging_ids.ids)
        packaging_str = ''
        i = 1
        for p in packaging:
            packaging_str += p.display_name + ': ' + str(p.qty)  
            if len(packaging) != i:
                packaging_str += ', ' 
            i += 1 
        return packaging_str
