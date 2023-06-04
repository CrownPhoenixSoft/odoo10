# -*- coding: utf-8 -*-

# Copyright (C) 2016 GRIMMETTE,LLC <info@grimmette.com>

import os
import re
from datetime import datetime, date
from cStringIO import StringIO
from zipfile import ZipFile, ZIP_DEFLATED
from lxml import etree
import tempfile
import copy
class XLSXEdit(object):
    def __init__(self, xlsx):
        self._zip_folder = self.extract_xlsx(xlsx)
        self._data = {}
        self._conf = {}
        self._conf['max_row_index'] = 0
        self._node_rd_attr = {}
        self._style_cat = {}
        self._style_header_data = {}
        self._zip_stream = StringIO()
        self._row_finder = re.compile(r'\d+$')
        self._column_finder = re.compile(r'\D+$')
        self._coord_re = re.compile('^[$]?([A-Z]+)[$]?(\d+)$')
        self._namespaces = {
            'ws': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
            'rel': 'http://schemas.openxmlformats.org/package/2006/relationships'
        }
        self._sheet_paths = self._get_sheet_locations()
        self._shared_strings = None
        self._shared_strings_root = None
        self._shared_strings_index = None
        self._COL_STRING_CACHE = {}
        self._STRING_COL_CACHE = {}
        for i in range(1, 18279):
            col = self._get_column_letter(i)
            self._STRING_COL_CACHE[i] = col
            self._COL_STRING_CACHE[col] = i
    def extract_xlsx(self,xlsx):
        tmp_dir = tempfile.gettempdir()
        zip_tmp_dir = tempfile.mkdtemp(prefix='xlsx.tmp.', dir=tmp_dir)
        z = ZipFile(xlsx)
        z.extractall(zip_tmp_dir)
        z.close()
        return zip_tmp_dir
    def _get_rd_attr(self,sheet_name):
        sheet_file = self._sheet_paths[sheet_name]
        xml = self._get_xml(sheet_file)
        pattern_params = {'row_data':self._conf['row_data']}
        pattern_rd = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_data)s"]' % pattern_params
        node_rd = xml.xpath(pattern_rd, namespaces=self._namespaces)
        if len(node_rd):
            self._node_rd_attr = dict(node_rd[0].attrib)
    def _get_style_header_data(self, conf_data):
        self._conf['header_data'] = {}
        self._conf['header_data']['company_reference'] = {}
        self._conf['header_data']['price_name_reference'] = {}
        self._conf['header_data']['currency_reference'] = {}
        self._conf['header_data']['print_date_reference'] = {}
        sheet_file = self._sheet_paths[conf_data['header_conf']['sheet_reference']]
        xml = self._get_xml(sheet_file)
        cell = conf_data['header_data']['company_reference']
        row_index = self._row_finder.search(cell).group()
        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params
        pattern_c = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_r = xml.xpath(pattern_r, namespaces=self._namespaces)
        if len(node_r) :
            node_rc = xml.xpath(pattern_c, namespaces=self._namespaces)
            if len(node_rc) :
                self._conf['header_data']['company_reference'] =  {cell: node_rc[0].get('s')} 
        cell = conf_data['header_data']['price_name_reference']
        row_index = self._row_finder.search(cell).group()
        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params
        pattern_c = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_r = xml.xpath(pattern_r, namespaces=self._namespaces)
        if len(node_r) :
            node_rc = xml.xpath(pattern_c, namespaces=self._namespaces)
            if len(node_rc) :
                self._conf['header_data']['price_name_reference'] =  {cell: node_rc[0].get('s')} 
        cell = conf_data['header_data']['currency_reference']
        row_index = self._row_finder.search(cell).group()
        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params
        pattern_c = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_r = xml.xpath(pattern_r, namespaces=self._namespaces)
        if len(node_r) :
            node_rc = xml.xpath(pattern_c, namespaces=self._namespaces)
            if len(node_rc) :
                self._conf['header_data']['currency_reference'] =  {cell: node_rc[0].get('s')} 
        cell = conf_data['header_data']['print_date_reference']
        row_index = self._row_finder.search(cell).group()
        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params
        pattern_c = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_r = xml.xpath(pattern_r, namespaces=self._namespaces)
        if len(node_r) :
            node_rc = xml.xpath(pattern_c, namespaces=self._namespaces)
            if len(node_rc) :
                self._conf['header_data']['print_date_reference'] =  {cell: node_rc[0].get('s')} 
    def update_conf(self, conf_data):
        if self._conf['header_data']['company_reference']:
            key1 = self._conf['header_data']['company_reference'].keys()[0]
            cell1 = conf_data['header_data']['company_reference']
            self._conf['header_data']['company_reference'][cell1] = self._conf['header_data']['company_reference'].pop(key1) 
            self._style_header_data[cell1] = self._conf['header_data']['company_reference'][cell1]
        if self._conf['header_data']['price_name_reference']:
            key2 = self._conf['header_data']['price_name_reference'].keys()[0]
            cell2 = conf_data['header_data']['price_name_reference']
            self._conf['header_data']['price_name_reference'][cell2] = self._conf['header_data']['price_name_reference'].pop(key2) 
            self._style_header_data[cell2] = self._conf['header_data']['price_name_reference'][cell2] 
        if self._conf['header_data']['currency_reference']:
            key3 = self._conf['header_data']['currency_reference'].keys()[0]
            cell3 = conf_data['header_data']['currency_reference']
            self._conf['header_data']['currency_reference'][cell3] = self._conf['header_data']['currency_reference'].pop(key3) 
            self._style_header_data[cell3] = self._conf['header_data']['currency_reference'][cell3]
        if self._conf['header_data']['print_date_reference']:
            key4 = self._conf['header_data']['print_date_reference'].keys()[0]
            cell4 = conf_data['header_data']['print_date_reference']
            self._conf['header_data']['print_date_reference'][cell4] = self._conf['header_data']['print_date_reference'].pop(key4) 
            self._style_header_data[cell4] = self._conf['header_data']['print_date_reference'][cell4]
    def write_conf(self, conf_data):
        sheet_file = self._sheet_paths[conf_data['header_conf']['sheet_reference']]
        xml = self._get_xml(sheet_file)
        header_location =  conf_data['header_conf']['header_reference']
        st, en = header_location.split(":")
        col_header,row_header = self.coordinate_from_string(st)
        col_data,row_data = self.coordinate_from_string(conf_data['data']['qty1'][0])
        self._conf['sheet_reference'] = conf_data['header_conf']['sheet_reference']
        self._conf['first_cell_header'] = st
        self._conf['col_header'] = col_header
        self._conf['row_header'] = row_header
        self._conf['row_data'] = row_data
        self._conf['show_categories'] = conf_data['filter']['show_categories']
        self._conf['show_categories_code'] = conf_data['filter']['show_categories_code']
        self._conf['show_level'] = conf_data['filter']['show_level']
        self._conf['show_autofilter'] = conf_data['filter']['show_autofilter']
        self._conf['show_images'] = conf_data['filter']['show_images']
        self._conf['wraptxt'] = conf_data['filter']['wraptxt']
        self._get_rd_attr(conf_data['header_conf']['sheet_reference'])
        self._get_style_header_data(conf_data)
        self._conf['cols'] = {}
        pattern = '/ws:worksheet/ws:cols'
        node_cols = xml.xpath(pattern, namespaces=self._namespaces)
        if len(node_cols):
            node_cols_child = node_cols[0].getchildren()
            if len(node_cols_child):
                for node_col in node_cols_child:
                    attr_min = node_col.get('min')
                    attr_max = node_col.get('max')
                    attr_min_max = ''.join([attr_min, ':', attr_max])
                    self._conf['cols'][attr_min_max] = [attr_min_max, int(attr_min), int(attr_max)]
        self._conf['mergeCells'] = {}
        pattern = '/ws:worksheet/ws:mergeCells'
        node_mergeCells = xml.xpath(pattern, namespaces=self._namespaces)
        if len(node_mergeCells):
            node_mergeCells_child = node_mergeCells[0].getchildren()
            if len(node_mergeCells_child):
                for node_mergeCell in node_mergeCells_child:
                    attr_ref = node_mergeCell.get('ref')
                    st, en = attr_ref.split(":")
                    col_1,row_1 = self.coordinate_from_string(st)
                    col_2,row_2 = self.coordinate_from_string(en)
                    col_1_ind= int(self.column_index_from_string(col_1))
                    col_2_ind= int(self.column_index_from_string(col_2))
                    self._conf['mergeCells'][attr_ref] = [attr_ref, col_1, row_1, col_2, row_2, col_1_ind, col_2_ind]
    def write(self, sheet, cell, value, level="0", category=False):
        if value not in (False, None) and type(value) not in (int, float, str, unicode, date, datetime):
            raise TypeError(u'Only None, int, float, str, unicode')
        if sheet not in self._data:
            self._data[sheet] = {}
        self._data[sheet][cell] = [value, str(level), category]
    def get_content(self):
        exclude_files = ['/%s' % e[1] for e in self._sheet_paths.items() if e[0] in self._data.keys()]
        exclude_files.append('/xl/sharedStrings.xml')
        exclude_files.append('/xl/workbook.xml')
        zip_file = self._create_base_zip(exclude_files=exclude_files)
        self._add_changes(zip_file)
        zip_file.writestr('xl/sharedStrings.xml', 
                          etree.tostring(self._shared_strings, 
                                         xml_declaration=True, 
                                         encoding="UTF-8", 
                                         standalone="yes"))
        zip_file.writestr('xl/workbook.xml', 
                          etree.tostring(self._get_xml('xl/workbook.xml'),
                                         xml_declaration=True, 
                                         encoding="UTF-8", 
                                         standalone="yes"))
        zip_file.close()
        return self._zip_stream.getvalue()
    def _get_xml(self, file_path):
        return etree.parse(os.path.join(self._zip_folder, file_path))
    def _init_shared_strings(self):
        self._shared_strings = self._get_xml('xl/sharedStrings.xml')
        self._shared_strings_root = self._shared_strings.xpath('/ws:sst', namespaces=self._namespaces)[0]
        self._shared_strings_index = int(self._shared_strings_root.attrib['uniqueCount'])
    def _add_shared_string(self, value):
        if self._shared_strings is None:
            self._init_shared_strings()
        node_t = etree.Element('t')
        node_t.text = value
        node_si = etree.Element('si')
        node_si.append(node_t)
        self._shared_strings_root.append(node_si)
        self._shared_strings_index += 1
        return (self._shared_strings_index - 1)
    def _get_sheet_locations(self):
        sheets_id = {}
        workbook_xml = self._get_xml('xl/workbook.xml')
        for sheet_xml in workbook_xml.xpath('/ws:workbook/ws:sheets/ws:sheet', namespaces=self._namespaces):
            sheet_name = sheet_xml.attrib['name']
            sheet_rid = sheet_xml.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            sheets_id[sheet_rid] = sheet_name
        paths = {}
        xml = self._get_xml('xl/_rels/workbook.xml.rels')
        for node in xml.xpath('/rel:Relationships/rel:Relationship', namespaces=self._namespaces):
            r_id = node.attrib['Id']
            path = os.path.join('xl', node.attrib['Target'])
            if r_id in sheets_id:
                sheet_label = sheets_id[r_id]
                paths[sheet_label] = path
        return paths    
    def _create_base_zip(self, exclude_files):
        zip_file = ZipFile(self._zip_stream, mode='w', compression=ZIP_DEFLATED, allowZip64=True)
        for path, dirs, files in os.walk(self._zip_folder):
            rel_path = path[len(self._zip_folder):]
            for file_name in files:
                if rel_path == '':
                    zip_name = file_name
                else:
                    zip_name = os.path.join(rel_path, file_name)
                if zip_name not in exclude_files:
                    zip_file.write(os.path.join(path, file_name), zip_name)
        return zip_file
    def _add_changes(self, zip_file):
        for sheet_name, data in self._data.items():
            sheet_file = self._sheet_paths[sheet_name]
            sheet_content = self._get_changed_sheet(sheet_file=sheet_file, data=data)
            zip_file.writestr(sheet_file, sheet_content)
    def _get_changed_sheet(self, sheet_file, data):
        xml = etree.parse(os.path.join(self._zip_folder, sheet_file))
        data_sort = [[cell,value] for (cell,value) in sorted(data.items())]
        for i in data_sort:
            self._change_cell(xml, i[0], i[1])
        if self._conf['show_autofilter']:
            self.add_autofilter(xml)
        return etree.tostring(xml, xml_declaration=True, encoding="UTF-8", standalone="yes")
    def _change_cell(self, xml, cell, values):
        value = values[0]
        row_index = self._row_finder.search(cell).group()
        value_type = type(value)
        if int(row_index) > self._conf['max_row_index']:
             self._conf['max_row_index'] = int(row_index) 
        pattern_params = {'row_index': row_index, 'cell': cell}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params
        pattern_c = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params
        node_r = xml.xpath(pattern_r, namespaces=self._namespaces)
        if len(node_r) :
            node_rc = xml.xpath(pattern_c, namespaces=self._namespaces)
            if len(node_rc) :
                node_c = node_rc[0] 
            else:
                    node_r_childs = node_r[0].getchildren()
                    if len(node_r_childs) :
                        n = 0 
                        for node_rci in node_r_childs:
                            attr_r = node_rci.attrib.get('r')
                            if node_rci.attrib.get('r') < cell:
                                if  n == (len(node_r_childs)-1):
                                    node_c = etree.SubElement(node_r[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell)
                                    node_r[0].insert(node_r[0].index(node_rci)+1, node_c)
                            if node_rci.attrib.get('r') > cell:
                                node_c = etree.SubElement(node_r[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell)
                                node_r[0].insert(node_r[0].index(node_rci), node_c)
                                break 
                            n += 1
                    else:
                        node_c = etree.SubElement(node_r[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell)
        else:
            if row_index > self._conf['row_data']:
                node_rd_attr = dict(self._node_rd_attr)
                node_rd_attr['r'] = row_index
                pattern_sh = '/ws:worksheet/ws:sheetData' % pattern_params
                node_sh = xml.xpath(pattern_sh, namespaces=self._namespaces)
                node_r = etree.SubElement(node_sh[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row', attrib=node_rd_attr)
                r_ind = int(row_index)
                r = True
                while r:
                    if r_ind > 0:
                        r_ind -= 1
                        pattern_params_rp = {'row_index': r_ind} 
                        pattern_r_prev = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params_rp
                        node_rp = xml.xpath(pattern_r_prev, namespaces=self._namespaces)
                        if len(node_rp) :
                            node_sh[0].insert(node_sh[0].index(node_rp[0])+1, node_r) 
                            r = False
                    else:
                        r = False
                node_c = etree.SubElement(node_r, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell)
            else:
                pattern_sh = '/ws:worksheet/ws:sheetData' % pattern_params
                node_sh = xml.xpath(pattern_sh, namespaces=self._namespaces)
                node_r = etree.SubElement(node_sh[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}row', r=row_index)
                r_ind = int(row_index)
                r = True
                while r:
                    if r_ind > 0:
                        r_ind -= 1
                        pattern_params_rp = {'row_index': r_ind} 
                        pattern_r_prev = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]' % pattern_params_rp
                        node_rp = xml.xpath(pattern_r_prev, namespaces=self._namespaces)
                        if len(node_rp) :
                            node_sh[0].insert(node_sh[0].index(node_rp[0])+1, node_r) 
                            r = False
                    else:
                        r = False
                node_c = etree.SubElement(node_r, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell)
        node_v = node_c.find('ws:v', namespaces=self._namespaces)
        if node_v is None:
            node_v = etree.Element('v')
            node_c.append(node_v)
        if value == None:
            node_c.remove(node_v)
            if node_c.attrib.get('t') == 's':
                del node_c.attrib['t']
        elif value_type in (unicode, str):
            value = str(self._add_shared_string(value))
            node_c.attrib['t'] = 's'
        else:
            if node_c.attrib.get('t') == 's':
                del node_c.attrib['t']
            if value_type == datetime:
                value = value.date()
                value_type = type(value)
            if value_type == date:
                value = (value - date(1899, 12, 30)).days
        node_v.text = unicode(value)
        if cell in self._style_header_data:
            node_c.set('s', self._style_header_data[cell])
        if int(row_index) >= self._conf['row_data']:
            col,row = self.coordinate_from_string(cell)
            node_row = node_c.getparent()
            if not (values[2]):
                if col in self._conf['column_data_style']:
                    node_c.set('s', self._conf['column_data_style'][col])
            else:
                style_cat = self._style_cat[int(values[1])]
                node_c.set('s', style_cat)
                for key in self._conf['list_column_out']:
                    if key != col:
                        cell_n = self.cell_from_coordinate(key, row_index)
                        pattern_params_cat = {'row_index': row_index, 'cell': cell_n}
                        pattern_cat = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row_index)s"]/ws:c[@r="%(cell)s"]' % pattern_params_cat
                        node_rc_cat = xml.xpath(pattern_cat, namespaces=self._namespaces)
                        if len(node_rc_cat) :
                            node_cn = node_rc_cat[0]
                            node_cn.set('s', style_cat) 
                        else:
                            node_row_childs = node_row.getchildren()
                            n = 0 
                            for node_rowci in node_row_childs:
                                attr_r = node_rowci.attrib.get('r')
                                if node_rowci.attrib.get('r') < cell_n:
                                    if  n == (len(node_row_childs)-1):
                                        node_cn = etree.SubElement(node_row, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell_n)
                                        node_row.insert(node_row.index(node_rowci)+1, node_cn)
                                        node_cn.set('s', style_cat)
                                if node_rowci.attrib.get('r') > cell_n:
                                    node_cn = etree.SubElement(node_row, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}c', r=cell_n)
                                    node_row.insert(node_row.index(node_rowci), node_cn)
                                    node_cn.set('s', style_cat)
                                    break 
                                n += 1
            if self._conf['show_level']: 
                if values[1] > 0:
                    node_row.set('outlineLevel', values[1])
    def add_autofilter(self, xml_sheet):
        pattern_sh = '/ws:worksheet/ws:sheetData'
        node_sh = xml_sheet.xpath(pattern_sh, namespaces=self._namespaces)[0]
        range_autoFilter = ''.join([self._conf['col_header'],
                                    str(self._conf['row_header']),':',
                                    self._conf['max_column'],
                                    str(self._conf['max_row_index'])
                                    ])
        parent_wsh = node_sh.getparent()
        node_autoFilter = etree.SubElement(parent_wsh, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}autoFilter', ref=range_autoFilter)
        parent_wsh.insert(parent_wsh.index(node_sh)+1, node_autoFilter)        
        xml_workbook = self._get_xml('xl/workbook.xml')
        definedName_text = ''.join([self._conf['sheet_reference'],'!',
                                    '$',self._conf['col_header'],
                                    '$',str(self._conf['row_header']),':',
                                    '$',self._conf['max_column'],
                                    '$',str(self._conf['max_row_index'])
                                    ])
        pattern_params_sheet = {'sheet_name': self._conf['sheet_reference']}
        pattern_sheet = '/ws:workbook/ws:sheets/ws:sheet[@name="%(sheet_name)s"]' % pattern_params_sheet
        node_sheet = xml_workbook.xpath(pattern_sheet, namespaces=self._namespaces)[0]
        localSheetId = node_sheet.getparent().index(node_sheet) 
        attr_dn = {'function':"false", 'name':"_xlnm._FilterDatabase", 'localSheetId':str(localSheetId), 'hidden':"1", 'vbProcedure':"false"}
        pattern_dns = '/ws:workbook/ws:definedNames'
        node_definedNames = xml_workbook.xpath(pattern_dns, namespaces=self._namespaces)
        if len(node_definedNames):
            node_definedName = etree.SubElement(node_definedNames[0], '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}definedName', attrib=attr_dn)
            node_definedNames[0].insert(0, node_definedName)        
            node_definedName.text = definedName_text
        else:
            pattern_wbsh = '/ws:workbook/ws:sheets'
            node_sheets = xml_workbook.xpath(pattern_wbsh, namespaces=self._namespaces)[0]
            parent_wbsh = node_sheets.getparent()
            node_definedNames = etree.SubElement(parent_wbsh, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}definedNames')
            parent_wbsh.insert(parent_wbsh.index(node_sheets)+1, node_definedNames)        
            node_definedName = etree.SubElement(node_definedNames, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}definedName', attrib=attr_dn)
            node_definedNames.insert(0, node_definedName)        
            node_definedName.text = definedName_text
        with open(os.path.join(self._zip_folder, 'xl/workbook.xml'), 'w') as workbook_file_out:
            xml_workbook.write(workbook_file_out)
    def add_format(self, col_product_name , theme='4'):
        xml = self._get_xml('xl/styles.xml')
        if col_product_name in self._conf['column_data_style']:
            style_name_ind = int(self._conf['column_data_style'][col_product_name])
        else:
            style_name_ind = 0
        pattern = '/ws:styleSheet/ws:cellXfs'
        node_cellxfx = xml.xpath(pattern, namespaces=self._namespaces)[0]
        node_xf_ntmpl = node_cellxfx.getchildren()[style_name_ind]
        pattern_fonts = '/ws:styleSheet/ws:fonts'
        node_fonts = xml.xpath(pattern_fonts, namespaces=self._namespaces)[0]
        node_font_ntmpl = node_fonts.getchildren()[int(node_xf_ntmpl.get('fontId'))]
        pattern_fills = '/ws:styleSheet/ws:fills'
        node_fills = xml.xpath(pattern_fills, namespaces=self._namespaces)[0]
        node_fill_ntmpl = node_fills.getchildren()[int(node_xf_ntmpl.get('fillId'))]
        pattern_borders = '/ws:styleSheet/ws:borders'
        node_borders = xml.xpath(pattern_borders, namespaces=self._namespaces)[0]
        node_border_ntmpl = node_borders.getchildren()[int(node_xf_ntmpl.get('borderId'))]
        tint_var = '-0.50'            
        for i in range(10):
            node_fonts.append(copy.deepcopy(node_font_ntmpl))
            node_fonts_n = node_fonts.getchildren()
            node_font_n = node_fonts_n[len(node_fonts_n)-1]
            node_b = node_font_n.find('ws:b', namespaces=self._namespaces)
            if node_b is None:
                node_b = etree.SubElement(node_font_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}b')
                node_font_n.insert(0, node_b) 
            node_sz = node_font_n.find('ws:sz', namespaces=self._namespaces)
            if node_sz is not None:
                if int(node_sz.get('val')) == 11:
                    font_inc = 1
                else:
                    font_inc = 2
                node_sz.set('val', str(int(node_sz.get('val'))+font_inc))
            node_color = node_font_n.find('ws:color', namespaces=self._namespaces)
            if node_color is None:
                node_color = etree.SubElement(node_font_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}color')
                node_font_name = node_font_n.find('ws:name', namespaces=self._namespaces)
                node_font_n.insert(node_font_n.index(node_font_name), node_color) 
            else:
                if 'rgb' in node_color.attrib.keys():
                    try:
                        del node_color.attrib["rgb"]
                    except:
                        pass                    
            if float(tint_var) >= 0.6:
                node_color.set('theme','1')
            else:
                node_color = node_font_n.find('ws:color', namespaces=self._namespaces)
                node_color.set('theme','0')
            node_fonts.set('count', str(int(node_fonts.get('count'))+1))
            node_fills.append(copy.deepcopy(node_fills.getchildren()[0]))
            node_fills_n = node_fills.getchildren()
            node_fill_n = node_fills_n[len(node_fills_n)-1]
            node_patternFill_n = node_fill_n.find('ws:patternFill', namespaces=self._namespaces)
            node_patternFill_n.set('patternType', "solid")
            node_fgColor = etree.SubElement(node_patternFill_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}fgColor', theme=theme, tint= tint_var)
            node_patternFill_n.append(node_fgColor)
            node_bgColor = etree.SubElement(node_patternFill_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}bgColor', indexed="64")
            node_patternFill_n.append(node_bgColor)
            tint_var = (str(float(tint_var) + 0.14))
            node_fills.set('count', str(int(node_fills.get('count'))+1))
            node_borders.append(copy.deepcopy(node_borders.getchildren()[0]))
            node_borders_n = node_borders.getchildren()
            node_border_n = node_borders_n[len(node_borders_n)-1]
            node_bottom_n = node_border_n.find('ws:bottom', namespaces=self._namespaces)
            node_bottom_n.set('style', "thin")
            node_color = etree.SubElement(node_bottom_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}color', indexed="64")
            node_bottom_n.append(node_color)
            node_borders.set('count', str(int(node_borders.get('count'))+1))
            node_cellxfx.append(copy.deepcopy(node_xf_ntmpl))
            node_cellxfx_n = node_cellxfx.getchildren()
            node_xf_n = node_cellxfx_n[len(node_cellxfx_n)-1]
            node_xf_n.set('fontId', str(len(node_fonts_n)-1))
            node_xf_n.set('fillId', str(len(node_fills_n)-1))
            node_xf_n.set('borderId', str(len(node_borders_n)-1))
            node_xf_n.set('applyFont', '1')
            node_xf_n.set('applyFill', '1')
            node_alignment = node_xf_n.find('ws:alignment', namespaces=self._namespaces)
            if node_alignment is None:
                node_alignment = etree.Element('alignment')
                node_alignment = etree.SubElement(node_xf_n, '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}alignment')
                node_xf_n.append(node_alignment)
            node_alignment.set('horizontal', 'left' )
            node_alignment.set('vertical', 'top' )
            node_cellxfx.set('count', str(int(node_cellxfx.get('count'))+1))
            self._style_cat[i] = str(len(node_cellxfx)-1)
        with open(os.path.join(self._zip_folder, 'xl/styles.xml'), 'w') as style_file_out:
            xml.write(style_file_out)
    def remove_culumn(self, sheet_name, column, row_start='1'):
        sheet_file = self._sheet_paths[sheet_name]
        xml = self._get_xml(sheet_file)
        column_index = int(self.column_index_from_string(column))
        pattern_params = {'row_start': row_start, 'column': column}
        pattern = '/ws:worksheet/ws:sheetData/ws:row[@r>="%(row_start)s"]/ws:c[starts-with(@r,"%(column)s")]' % pattern_params
        node_c = xml.xpath(pattern, namespaces=self._namespaces)
        if len(node_c):
            for cell in node_c:
                cell.getparent().remove(cell)
        pattern = '/ws:worksheet/ws:cols'
        node_cols = xml.xpath(pattern, namespaces=self._namespaces)
        if len(node_cols):
            node_cols_child = node_cols[0].getchildren()
            if len(node_cols_child):
                for node_col in node_cols_child:
                    attr_min = int(node_col.get('min'))
                    attr_max = int(node_col.get('max'))
                    attr_min_max = ''.join([str(attr_min), ':', str(attr_max)])
                    if self._conf['cols'][attr_min_max]:
                        attr_min_o = self._conf['cols'][attr_min_max][1]  
                        attr_max_o = self._conf['cols'][attr_min_max][2]
                        if attr_min_o <= column_index and column_index <= attr_max_o:
                            if attr_min_o == attr_max_o:
                                node_col.getparent().remove(node_col)
                            else:
                                if attr_min == attr_max:
                                    node_col.getparent().remove(node_col)
                                else:
                                    node_col.set('max',str(attr_max-1)) 
                                    attr_min_max_n = ''.join([str(attr_min), ':',
                                                              str(attr_max - 1)
                                                              ])
                                    self._conf['cols'][attr_min_max_n] = self._conf['cols'].pop(attr_min_max)
                        if attr_min_o > column_index:
                            node_col.set('min',str(attr_min-1)) 
                            node_col.set('max',str(attr_max-1)) 
                            attr_min_max_n = ''.join([str(attr_min - 1), ':',
                                                      str(attr_max - 1)
                                                      ])
                            self._conf['cols'][attr_min_max_n] = self._conf['cols'].pop(attr_min_max)
        pattern = '/ws:worksheet/ws:mergeCells'
        node_mergeCells = xml.xpath(pattern, namespaces=self._namespaces)
        if len(node_mergeCells):
            node_mergeCells_child = node_mergeCells[0].getchildren()
            if len(node_mergeCells_child):
                for node_mergeCell in node_mergeCells_child:
                    attr_ref = node_mergeCell.get('ref')
                    st, en = attr_ref.split(":")
                    col_1,row_1 = self.coordinate_from_string(st)
                    col_2,row_2 = self.coordinate_from_string(en)
                    col_1_ind= int(self.column_index_from_string(col_1))
                    col_2_ind= int(self.column_index_from_string(col_2))
                    if self._conf['mergeCells'][attr_ref]:
                        col_1_o = self._conf['mergeCells'][attr_ref][1]  
                        row_1_o = self._conf['mergeCells'][attr_ref][2]
                        col_2_o = self._conf['mergeCells'][attr_ref][3]
                        row_2_o = self._conf['mergeCells'][attr_ref][4]
                        col_1_o_ind= self._conf['mergeCells'][attr_ref][5]
                        col_2_o_ind= self._conf['mergeCells'][attr_ref][6]
                        if col_1_o_ind == column_index:
                            node_mergeCell.getparent().remove(node_mergeCell) 
                        else:
                            if col_1_o_ind < column_index and column_index <= col_2_o_ind:
                                attr_ref_n = ''.join([col_1,
                                                      str(row_1),':',
                                                      self.get_column_letter(col_2_ind - 1),
                                                      str(row_2)
                                                      ])
                                node_mergeCell.set('ref', attr_ref_n) 
                                self._conf['mergeCells'][attr_ref_n] = self._conf['mergeCells'].pop(attr_ref)
                        if col_1_o_ind > column_index:
                            attr_ref_n = ''.join([self.get_column_letter(col_1_ind - 1),
                                                  str(row_1),':',
                                                  self.get_column_letter(col_2_ind - 1),
                                                  str(row_2)
                                                  ])
                            node_mergeCell.set('ref', attr_ref_n)
                            self._conf['mergeCells'][attr_ref_n] = self._conf['mergeCells'].pop(attr_ref)
        with open(os.path.join(self._zip_folder, sheet_file), 'w') as sheet_file_out:
            xml.write(sheet_file_out)
    def shift_coordinate(self, sheet_name, res_data_ind_out):
        sheet_file = self._sheet_paths[sheet_name]
        xml = self._get_xml(sheet_file)
        for i in res_data_ind_out:
            if i[3] == False:
                column_false = self.get_column_letter(i[1]) 
                pattern = '/ws:worksheet/ws:sheetData/ws:row'
                node_r = xml.xpath(pattern, namespaces=self._namespaces)
                for r in node_r:
                    childs = r.getchildren()
                    for c in childs:
                        coord  = c.get('r')
                        if coord > column_false:
                            col,row = self.coordinate_from_string(coord)
                            col_ind = self.column_index_from_string(col)  
                            new_col = self.get_column_letter(col_ind -1) 
                            new_r = ''.join([new_col,str(row)])
                            c.set('r', new_r)
        pattern_params_r = {'row': int(res_data_ind_out[0][2])}
        pattern_r = '/ws:worksheet/ws:sheetData/ws:row[@r="%(row)s"]' % pattern_params_r
        node_rd = xml.xpath(pattern_r, namespaces=self._namespaces)
        self._conf['column_data_style'] = {}
        if len(node_rd):
            rd_childs = node_rd[0].getchildren()
            for rd in rd_childs:
                cell_r = rd.get('r')
                cell_r_letter,ind = self.coordinate_from_string(cell_r)
                cell_s = rd.get('s')
                self._conf['column_data_style'][cell_r_letter] = cell_s
        max_column = 0
        self._conf['list_column_out'] = []
        for cd in res_data_ind_out:
            if cd[3]:
                self._conf['list_column_out'].append(self.get_column_letter(cd[1]))
                if cd[1] > max_column:
                    self._conf['max_column'] = self.get_column_letter(cd[1])
        with open(os.path.join(self._zip_folder, sheet_file), 'w') as sheet_file_out:
            xml.write(sheet_file_out)
    def coordinate_from_string(self, coord_string):
        match = self._coord_re.match(coord_string.upper())
        if not match:
            msg = 'Invalid cell coordinates (%s)' % coord_string
            raise ValueError(msg)
        column, row = match.groups()
        row = int(row)
        if not row:
            msg = "There is no row 0 (%s)" % coord_string
            raise ValueError(msg)
        return (column, row)
    def _get_column_letter(self, col_idx):
        if not 1 <= col_idx <= 18278:
            raise ValueError("Invalid column index {0}".format(col_idx))
        letters = []
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx, 26)
            if remainder == 0:
                remainder = 26
                col_idx -= 1
            letters.append((chr(remainder+64)).decode("utf-8"))
        return ''.join(reversed(letters))
    def get_column_letter(self, idx,):
        try:
            return self._STRING_COL_CACHE[idx]
        except KeyError:
            raise ValueError("Invalid column index {0}".format(idx))
    def column_index_from_string(self, str_col):
        try:
            return self._COL_STRING_CACHE[str_col.upper()]
        except KeyError:
            raise ValueError("{0} is not a valid column name".format(str_col))
    def cell_from_index(self, col_ind, row_ind):
        col_letter = self.get_column_letter(col_ind) 
        return ''.join([col_letter,str(row_ind)])
    def cell_from_coordinate(self, col_letter, row_ind):
        return ''.join([col_letter,str(row_ind)])
    def column_compare(self, cell_1, cell_2):
        col_1_letter, row_1_ind = self.coordinate_from_string(cell_1)
        col_1_ind = self.column_index_from_string(col_1_letter)
        col_2_letter, row_2_ind = self.coordinate_from_string(cell_2)
        col_2_ind = self.column_index_from_string(col_2_letter)
        if col_1_ind == col_2_ind:
            return True
        else:
            return False
