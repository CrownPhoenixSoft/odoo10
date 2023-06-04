# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
# from odoo import http


# class ProductQrCode(http.Controller):
#     @http.route('/product_qr_code/product_qr_code/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_qr_code/product_qr_code/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_qr_code.listing', {
#             'root': '/product_qr_code/product_qr_code',
#             'objects': http.request.env['product_qr_code.product_qr_code'].search([]),
#         })

#     @http.route('/product_qr_code/product_qr_code/objects/<model("product_qr_code.product_qr_code"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_qr_code.object', {
#             'object': obj
#         })
