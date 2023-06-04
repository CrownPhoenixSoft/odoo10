# -*- coding: utf-8 -*-
#################################################################################
#
#
#################################################################################

{
    'name': 'Pandora UAE VAT Account Base',
    'category': 'Accounting',
    'version': '1.0',
    'summary': '',
    'description': """ """,
    'author': 'Pandoratech',
    'website': 'https://pandoratech.ae',
    'price': '',
    'currency': '',
    'depends': ['base', 'account','professional_templates','sale_discount_total'],
  
   
    "data": [

        'invoice/custom_template.xml',
         'invoice/invoice_lines.xml',

        'invoice/invoice_lines_no_layout.xml',



              'views/sale_view.xml',
             'views/account_invoice_view.xml',
             'views/purchase_view.xml',
             'report/sale_report_template.xml',
             'report/purchase_report_template.xml',
             'report/invoice_report.xml',
             'reports.xml',
             "views/account_invoice_thermal_report_template.xml",
             ],
    'qweb': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
