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
    'name': 'Sale Discount on Total Amount Margin Control',
    'version': '10.0.1.0',
    'category': 'Sales Management',
    'summary': "Module to manage margin on product price in Sale as an specific amount of percentage.",
    "website": "https://acespritech.com/",
    "author": "Acespritech Solutions Pvt. Ltd.",
    "license": "AGPL-3",

    'description': """
                Sale Margin Control On Products
                """,
    'depends': [
                'sale_discount_total',
                'sale_margin',
                ],
    'data': [
        'views/res_config_view.xml',
            ],
    'demo': [],
    'images': ['static/description/icon.png'],
    'application': True,
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
