# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2016 GRIMMETTE,LLC <info@grimmette.com>

{
    'name': 'Professional Pricelists Excel (XLSX,XLSM)',
    'version': '1.9',
    'category': 'Sales',
    'summary': 'This module generates a Professional Pricelists in MS Excel format (XLSX,XLSM)',
    'price': 150.00,
    'currency': 'EUR',
    "license": "OPL-1",     
    'description': """
Professional Pricelist Excel.
====================================
Generates a Pricelists in MS Excel format (XLSX,XLSM).

    """,
    'author': 'GRIMMETTE,LLC',
#    'website': 'http://www.grimmette.com',
    'support': 'info@grimmette.com',
    'depends': ['product','document','delivery'],
    'images': ['static/description/example0.png'],
    'data': [
        'security/ir.model.access.csv',
        'views/pricelist_excel_views.xml',
        'views/product_views.xml',
        'views/web_export_xlsx_view.xml',
        'wizard/product_price_wizard_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}
