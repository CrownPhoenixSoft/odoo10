# -*- coding: utf-8 -*-
{
    'name': "employee_case_report",

    'summary': """
        Module for Employee case report""",

    'description': """
       This module will help to get the employee case report 
    """,

    'author': "Employee Case Report",
    'website': "http://www.clicktohub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '10.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','hr','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/view_employee_case_report.xml',
        'views/view_hr_employee.xml',
        'report/employee_case_report.xml',
        'report/reports.xml',
        'views/sequence.xml',
        'views/actions.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
