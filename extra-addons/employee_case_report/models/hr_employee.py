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


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    case_report_count = fields.Integer(string="Case Reports", compute='display_employee_case_count')
    damage_amount = fields.Float(compute='display_damage_amount')

    def display_employee_case_count(self):
        for record in self:
            employee_case_report_count = record.env['employee_case_report.employee_case_report'].search([('employee_id', '=', record.id)])
            if employee_case_report_count:
                record.case_report_count = len(employee_case_report_count)
            else:
                record.case_report_count = 0

    def display_damage_amount(self):
        '''Display Damage Amount'''
        for record in self:
            employees = record.env['employee_case_report.employee_case_report'].search(
                [('employee_id.id', '=', record.id), ('damage_amount', '!=', 0)])
            if employees:
                damage_amounts = [item.damage_amount for item in employees]
                record.damage_amount = sum(damage_amounts)
            else:
                record.damage_amount = 0

