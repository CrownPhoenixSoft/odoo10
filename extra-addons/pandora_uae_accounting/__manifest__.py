# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# Copyright (C) 2020 Pandora Tech LLC (<http://pandoratech.ae>)

{
    'name': 'U.A.E. - Accounting',
    'author': 'Pandora Tech LLC',
    'category': 'Localization',
    'description': """
United Arab Emirates accounting chart and localization.
=======================================================

    """,
    'depends': ['base', 'account'],
    'data': [
             'data/pandora_uae_accounting_data.xml',
             'data/account_data.xml',
             'data/pandora_uae_accounting_chart_data.xml',
             'data/account.account.template.csv',
             'data/pandora_uae_accounting_chart_post_data.xml',
             'data/account_tax_template_data.xml',
             'data/fiscal_templates_data.xml',
             'data/account_chart_template_data.xml',
             'views/report_invoice_templates.xml',
    ],
}
