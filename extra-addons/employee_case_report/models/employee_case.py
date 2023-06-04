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
from datetime import date
import lxml, json
from lxml import etree

class EmployeeCaseReport(models.Model):
    _name = 'employee_case_report.employee_case_report'
    _description = 'Employee Case Report'
    _inherit = ['mail.thread']
    _rec_name = 'employee_id'

    description = fields.Text()
    name = fields.Char()
    status = fields.Selection(
        [('draft', 'Draft'), ('waiting_response', 'Waiting Response'), ('waiting_manager_action', 'Waiting Manager Action'),
         ('accountant_action', 'Accountant Action'), ('done', 'Done'), ('cancelled', 'Cancelled'), ],
        default='draft')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user.id)

    # Officer Group
    officer_user_id = fields.Many2one('res.users', string='Officer Name', track_visibility=True)
    case_date = fields.Date(string='Case Date', compute="_compute_case_date")
    sale_id = fields.Many2one('sale.order', string="Related Sale Order", track_visibility=True)
    partner_id = fields.Many2one('res.partner', string="Related Customer", track_visibility=True)
    created_reason = fields.Text(string='Created Reason', track_visibility=True)
    damage_amount = fields.Float(string='Damage Amount', track_visibility=True)
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department',string='Department', track_visibility=True)
    employee_id = fields.Many2one('hr.employee', string='Employee Name', track_visibility=True, required="1")
    employee_ids = fields.Many2many('hr.employee', 'employee_rel', 'employee_id', 'employee_rel2',
                                    string='Employee IDs')
    # Employee section
    response_date = fields.Date(string='Response Date')
    employee_response = fields.Text(string='Employee Response', track_visibility=True)

    # Manager Section
    manager_user_id = fields.Many2one('res.users', string='Manager Name', track_visibility=True)
    # manager_name = fields.Char(string='Manager Name',track_visibility=True)
    action_type = fields.Selection(
        [('first_warning', 'First Warning'), ('second_warning', 'Second Warning'), ('final_warning', 'Final Warning'),
         ('deduct_from_salary', 'Deduct from salary'), ], string='Action Type', track_visibility=True)
    action_date = fields.Date(string='Action Date', readonly="1")
    manager_response = fields.Text(string='Manager Response')

    def _compute_case_date(self):
        '''COmpute Case Date'''
        for record in self:
            record.case_date = date.today()

    def submit_response(self):
        self.status = 'waiting_response'
        self.response_date = date.today()

    def reset_to_draft(self):
        self.status = 'draft'

    def change_to_done(self):
        self.status = 'done'

    def approve(self):
        self.status = 'accountant_action'
        self.action_date = date.today()

    def reject(self):
        self.status = 'cancelled'
        self.action_date = date.today()

    def submit_employee_response(self):
        self.status = 'waiting_manager_action'

    def print_pdf_report(self):
        '''Print QWEB/PDF Report '''
        res = {
            'type': 'ir.actions.report.xml',
            'report_name': 'employee_case_report.report_employee_case',
        }
        return res

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            employee_ids = []
            employee_ids.append(self.employee_id.id)
            self.employee_ids = employee_ids

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'employee_case_report.employee_case_report') or 'New'
        result = super(EmployeeCaseReport, self).create(vals)
        return result
