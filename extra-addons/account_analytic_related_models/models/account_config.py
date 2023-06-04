# -*- coding: utf-8 -*-
#################################################################################
# Copyright 2020 ClicktoHub (<https://clicktohub.com>).
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################
from odoo import fields, models

class AccountConfigSettings(models.TransientModel):
    _inherit = 'account.config.settings'

    analytic_account_employee = fields.Boolean("Create Employee Analytic Account.")
    analytic_account_fleet = fields.Boolean("Create Fleet Analytic Account.")