# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import models, fields, api, _


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: