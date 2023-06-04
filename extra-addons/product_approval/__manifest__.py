# -*- coding: utf-8 -*-
{
    "name": "Product Approval",
    'summary': 'Product Approval workflow',
    "description": """This module will allows you to approve or refuse product only by product manager.""",

    'author': 'iPredict IT Solutions Pvt. Ltd.',
    'website': 'http://ipredictitsolutions.com',
    "support": "ipredictitsolutions@gmail.com",

    "category": "Product",
    'version': '10.0.0.1.0',
    "depends": ["product"],

    "data": [
        "data/product_approve_mail_template.xml",
        "security/security.xml",
        "views/product_template.xml",
    ],

    'license': "OPL-1",
    "currency": "EUR",
    "price": 15.00,

    "installable": True,

    "images": ['static/description/main.png'],
}
