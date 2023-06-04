# -*- coding: utf-8 -*-
{
    'name': "SW - Invoice Source Document Button",
    'summary': """
        This module add "Source Document" button to Vendor Bills & Invoices""",
    'author': "Smart Way Business Solutions",
    'website': "https://www.smartway.co",
    'license': 'Other proprietary',
    'category': 'Accounting',
    'version': '10.0.1.0',
    'depends': ['base','account','purchase','sale'],
    'data': [
        'views/account_invoice_views.xml',
    ],
    'images':  ["static/description/image.png"],
    'installable': True,
    'auto_install': False,
    'application':False,
}