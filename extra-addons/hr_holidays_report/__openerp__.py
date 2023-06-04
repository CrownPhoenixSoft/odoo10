# -*- coding: utf-8 -*-

# Part of Probuse Consulting Service Pvt Ltd. See LICENSE file for full copyright and licensing details.

{
    'name':'HR Holidays Leave/Allocation Report',
    'version':'1.0',
    'price': 10.0,
    'currency': 'EUR',
    'category':'Human Resources',
    'license': 'Other proprietary',
    'description': """
                HR Holidays Report:
                    - Holidays Leave Request Report
                    - Holidays Leave Allocation Request Report
                    - Leave Report
            """,
    'author' : 'Probuse Consulting Service Pvt. Ltd.',
    'website': 'www.probuse.com',
    'depends': ['hr_holidays'],
    'data':['report/hr_holidays_leave_report.xml'],
    'installable': True,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
