# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

from odoo import models, fields, api


class ProductQrReport(models.AbstractModel):
    _name = 'report.product.report_product_qr'

    @api.model
    def render_html(self, docids, data=None):
        report_obj = self.env['report']
        product_template = self.env['product.template'].browse(docids)
        docargs = {
            'doc_ids': docids,
            'docs': product_template,
        }
        return report_obj.render('product_qr_code.report_product_qr', docargs)
