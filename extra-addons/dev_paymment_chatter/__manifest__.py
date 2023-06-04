# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 Devintelle Software Solutions (<http://devintellecs.com>).
#
##############################################################################

{
    'name': 'Payment Chatter & followers',
    'version': '1.0',
    'category': 'Accounting',
    'sequence': 1,
    'description': """
        Apps will help to add chatter and followers in Payment/Voucher.
    """,
    'summary':"""Apps will help to add chatter and followers in Payment/Voucher.""",
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com/',
    'depends': ['account'],
    'data': [
        'views/account_payment.xml',
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price':12.0,
    'currency':'EUR',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
