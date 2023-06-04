# -*- encoding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Cash & Bank Statements CSV Import',
    'category': 'Accounting & Finance',
    'summary': 'Import Cash & Bank Statements from CSV',
    'website': 'http://dvit.me/',
    'version': '10.0.2.2',
    'license': 'AGPL-3',
    'author': 'DVIT.ME',
    'description': "",
    'data': [
        'views/account_csv.xml',
    ],
    'depends': [
        'account_bank_statement_import',
    ],
    'external_dependencies': {
        'python': [
            'unicodecsv',
            'chardet',
        ]
    },
    'images': [
        'static/description/icon.png',
    ],
    'installable': True,
    'application': False,
}
