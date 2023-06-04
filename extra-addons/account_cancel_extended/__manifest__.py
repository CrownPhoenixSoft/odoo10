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
    "name": "Account Cancel Extended",
    "category": "Accounting",
    "website": "https://acespritech.com/",
    "author": "Acespritech Solutions Pvt. Ltd.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "account",
        "account_cancel",
        "account_accountant",
    ],
    "data": [
             "security/security.xml",
             "views/account_view.xml",
    ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: