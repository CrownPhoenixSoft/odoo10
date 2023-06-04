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
    'name': 'Account custom filter',
    'category': 'Accounting',
    'summary': 'Allow user to filter according to Balance sheet and Profit & Loss.',
    'description': """
Allow user to filter according to Balance sheet and Profit & Loss..
""",
    'author': "Acespritech Solutions Pvt. Ltd.",
    'website': "http://www.acespritech.com",
    'version': '1.0',
    'depends': ['account', 'base'],
    'images': ['static/description/main_screenshot.png'],
    'data': [
        'views/account_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
