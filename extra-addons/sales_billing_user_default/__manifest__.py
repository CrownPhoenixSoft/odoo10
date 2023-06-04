# Copyright 2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Sales Billing User Account',
    'summary': 'Setting default customer and payment journal.',
    'description' : 'Setting default customer and payment journal.',
    'version': '10.0.1.0.0',
    'category': 'Sale',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
    'depends': [
        'base',
        'sale',
        'account',
    ],
    'data': [
        'views/res_users_view.xml'
    ],
}
