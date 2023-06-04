# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Scrap Product Access',
    'version': '1.1',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'category': 'invetory',
    'description': """
    """,
    'website': 'http://www.acespritech.com',
    'summary': 'Only invetory manager can validate the scrap product move',
    'depends': ['stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/scrap_product_access_view.xml',
        'views/stock_scrap_report_template.xml',
        'report/scrap_print.xml',
    ],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=
