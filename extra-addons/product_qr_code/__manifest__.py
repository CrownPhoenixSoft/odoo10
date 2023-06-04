# -*- coding: utf-8 -*-
{
    'name': "product_qr_code",

    'summary': """
        Product QR Code""",

    'description': """
       Scan Product QR Code 
    """,

    'author': "ClicktoHub",
    'website': "http://www.clicktohub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '10.0.1',
    'images': ['static/description/banner.jpg'],

    # any module necessary for this one to work correctly
    'depends': ['base','website','website_sale','sale'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/product_qr_report.xml',
        'report/reports.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
