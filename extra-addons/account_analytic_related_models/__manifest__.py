# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': "Account Analytic Related Models",
    'version': '10.0.0.0.0',
    'description': """This module is used to account analytic related models.""",
    'summary': 'This module is used to account analytic related models.',
    'website': "https://clicktohub.com",
    'author': 'ClicktoHub',
    'depends': ['web', 'account','analytic','fleet','hr','project'],
    'data': [
        'views/account_config.xml',
        'views/analytic_account_view.xml',
    ],
    'qweb': [],
    "installable": True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: