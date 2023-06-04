# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from qrcode import base
from odoo import models, fields, api
import base64
from io import BytesIO
import qrcode
import base64
from odoo.http import request
import webbrowser



class ProductTemplate(models.Model):
    _inherit = 'product.template'


    qr_image = fields.Binary("QR Code",compute="generate_qr_code")
    # company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company.id)

    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        base_url = request.env['ir.config_parameter'].get_param('web.base.url') + '/shop/product/' + str(self.id)
        qr.add_data(base_url)
        qr.make(fit=True)
        img = qr.make_image()
        temp = BytesIO()
        img.save(temp)
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_image = qr_image
