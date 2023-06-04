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
    "name": "Product Margin Custom",
    "category": "Acccount",
    "website": "https://acespritech.com/",
    "author": "Acespritech Solutions Pvt. Ltd.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base","product_margin"],
    "data": [
             'views/product_margin_custom_view.xml',
             'views/product_product_views.xml'
            ],
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: