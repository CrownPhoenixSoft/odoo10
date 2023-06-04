# Copyright 2018 Tecnativa - Carlos Dauden
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Register Invoice and Print',
    'summary': 'Register invoice and print invoice from the same button.',
    'description': 'Register invoice and print the report at the same time.',
    'version': '10.0.1.0.1',
    'category': 'Accounting',
    # 'website': 'https://github.com/OCA/sale-workflow',
    # 'author': 'Tecnativa, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': True,
    'installable': True,
    'auto_install': False,
    'depends': [
        'account','sales_billing_user_default','professional_templates',
    ],
    'data': [
        'views/account_payment_view.xml'
    ],
}
